import json
import os
import tempfile
import zipfile
from contextlib import asynccontextmanager
from io import StringIO

import anyio
import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.background import BackgroundTasks

from app.config import APP_CONFIG, SPRING_DEPENDENCIES, SPRING_SERVICE_URL
from app.generate_controller_springboot.generate_controller_springboot import (
    generate_springboot_controller_file,
)
from app.generate_frontend.create.create_page_views import generate_create_page_views
from app.generate_frontend.create.generate_create_page_django import (
    generate_forms_create_page_django,
    generate_html_create_pages_django,
)
from app.generate_frontend.delete.delete_page_views import generate_delete_page_views
from app.generate_frontend.edit.edit_page_views import generate_edit_page_views
from app.generate_frontend.edit.generate_edit_page_django import (
    generate_html_edit_pages_django,
)
from app.generate_frontend.generate_landing_page import (
    generate_landing_page_html,
    generate_landing_page_views,
)
from app.generate_frontend.read.generate_read_page_django import (
    generate_html_read_pages_django,
)
from app.generate_frontend.read.read_page_views import generate_read_page_views
from app.generate_repository.generate_repository import generate_repository_java
from app.generate_runner.generate_runner import (
    generate_springboot_linux_runner,
    generate_springboot_window_runner,
)
from app.generate_service_springboot.generate_service_springboot import (
    generate_sequence_service_java,
    generate_service_java,
)
from app.generate_swagger.generate_swagger import (
    generate_swagger_config,
)
from app.model import (
    ConvertRequest,
    DataResult,
    DuplicateChecker,
    Style,
)
from app.models.elements import (
    ClassObject,
    ModelsElements,
    RequirementsElements,
    UrlsElement,
    ViewsElements,
)
from app.parse_json_to_object_seq import ParseJsonToObjectSeq
from app.utils import (
    is_valid_java_package_name,
    is_valid_python_identifier,
    logger,
    remove_file,
    render_project_django_template,
    render_template,
    translate_to_cat,
)


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    instrumentator.expose(app)
    yield


app = FastAPI(**APP_CONFIG, lifespan=lifespan)
instrumentator = Instrumentator().instrument(app)
BASE_STATIC_TEMPLATES_DIR = os.path.join("app", "templates", "django_app")
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CSS_DIR = os.path.join(CUR_DIR, "templates", "css")

error_counter = Counter(
    "convert_errors_total", "Total number of errors by message", ["error_message"]
)

parse_latency = Histogram(
    "parse_latency_seconds", "Histogram of parsing durations in seconds", ["diagram"]
)


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, FastAPI World!"}


@app.post("/convert")
async def convert(
    request: ConvertRequest,
    background_tasks: BackgroundTasks,
) -> Response:
    filenames = request.filename
    contents = request.content
    if len(filenames) != len(contents):
        raise HTTPException(
            status_code=400, detail="number of Filename and Content is incosistent"
        )

    project_name = request.project_name
    try:
        if request.project_type == "django":
            tmp_zip_path = await convert_django(
                project_name, filenames, contents, request.style_theme
            )
        else:
            tmp_zip_path = await convert_spring(
                project_name.lower(), request.group_id.lower(), filenames, contents
            )
        background_tasks.add_task(remove_file, tmp_zip_path)

        return FileResponse(
            path=tmp_zip_path,
            filename=project_name + ".zip",
            media_type="application/zip",
        )

    except ValueError as ex:
        ex_str = str(ex)
        error_counter.labels(error_message=translate_to_cat(ex_str)).inc()
        logger.warning(
            "Error occurred at parsing: " + ex_str.replace("\n", " "), exc_info=True
        )
        raise HTTPException(status_code=422, detail=ex_str)

    except HTTPException:
        raise

    except Exception as ex:
        ex_str = str(ex)
        logger.warning(
            "Unknown error occured: " + ex_str.replace("\n", " "), exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Unknown error occured: {ex_str}\nPlease try again later",
        )


async def convert_django(
    project_name: str, filenames: list[str], contents: list[list[str]], style: Style
) -> str:
    tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp_zip_path = tmp_zip.name
    try:
        fetched = fetch_data(filenames, contents)
        response_content_models = fetched["models"]
        response_content_views = fetched["views"]
        writer_models = fetched["model_element"]
        writer_requirements = RequirementsElements()

        writer_url = UrlsElement()
        writer_url.set_classes(writer_models.get_classes())

        file_elements = (writer_models, writer_requirements, writer_url)
        generate_file_to_be_downloaded(
            project_name=project_name,
            models=response_content_models,
            views=response_content_views,
            file_elements=file_elements,
            zipfile_path=tmp_zip_path,
        )

        css_file = os.path.join(CSS_DIR, f"{style}.css")
        with zipfile.ZipFile(tmp_zip_path, "a", zipfile.ZIP_DEFLATED) as zipf:
            async with await anyio.open_file(css_file) as cssf:
                zipf.writestr("static/css/style.css", await cssf.read())

        tmp_zip.close()
        return tmp_zip_path

    except ValueError:
        tmp_zip.close()
        remove_file(tmp_zip_path)
        raise

    except Exception:  # Some other exception that might be missed
        tmp_zip.close()
        remove_file(tmp_zip_path)
        raise

    finally:
        files = [
            f"{project_name}_models.py",
            f"{project_name}_views.py",
        ]
        for file in files:
            if os.path.exists(file):
                os.remove(file)


async def convert_spring(
    project_name: str, group_id: str, filenames: list[str], contents: list[list[str]]
) -> str:
    package_name = f"{project_name}.{group_id}"
    if not is_valid_java_package_name(package_name):
        msg = f"Invalid Java package name: {package_name}"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)

    tmp_zip_path = await initialize_springboot_zip(project_name, group_id)

    src_path = group_id.replace(".", "/") + "/" + project_name

    with zipfile.ZipFile(tmp_zip_path, "a", zipfile.ZIP_DEFLATED) as zipf:
        # put swagger config to zip
        swagger_config_content = generate_swagger_config(group_id, project_name)
        zipf.writestr(
            write_springboot_path(src_path, "config", "Swagger"),
            swagger_config_content,
        )

        # put runner to zip
        windows_runner = generate_springboot_window_runner()
        linux_runner = generate_springboot_linux_runner()
        zipf.writestr("run.bat", windows_runner)
        zipf.writestr("run.sh", linux_runner)

        data = fetch_data(filenames, contents)

        writer_models = data["model_element"]

        model_files = writer_models.print_springboot_style(project_name, group_id)

        # Specific line of code to generate HomeController for Swagger Redirection
        zipf.writestr(
            write_springboot_path(src_path, "controller", "Home"),
            render_template(
                "springboot/HomeController.java.j2",
                {"group_id": group_id, "project_name": project_name},
            ),
        )

        for class_object in writer_models.get_classes():
            if class_object.get_is_public():
                zipf.writestr(
                    write_springboot_path(
                        src_path, "controller", class_object.get_name()
                    ),
                    generate_springboot_controller_file(
                        project_name, class_object, group_id
                    ),
                )

            zipf.writestr(
                write_springboot_path(src_path, "service", class_object.get_name()),
                generate_service_java(project_name, class_object, group_id),
            )

            zipf.writestr(
                write_springboot_path(src_path, "model", class_object.get_name()),
                model_files[class_object.get_name()],
            )
            zipf.writestr(
                write_springboot_path(src_path, "repository", class_object.get_name()),
                generate_repository_java(project_name, class_object, group_id),
            )
        zipf.writestr(
            write_springboot_path(src_path, "service", "SequenceService"),
            generate_sequence_service_java(
                project_name, data["views_element"], group_id
            ),
        )

    return tmp_zip_path


def write_springboot_path(src_path: str, file: str, class_name: str) -> str:
    if file == "model":
        return f"src/main/java/{src_path}/{file}/{class_name}.java"
    return f"src/main/java/{src_path}/{file}/{class_name}{file.capitalize()}.java"


def check_duplicate(
    class_objects: dict[str, ClassObject],
    class_object_name: str,
    duplicate_class_method_checker: DuplicateChecker,
) -> DuplicateChecker:
    class_object = class_objects.get(class_object_name, None)
    if not class_object:
        return duplicate_class_method_checker
    for class_method_object in class_objects[class_object_name].get_methods():
        key = (class_object_name, class_method_object.get_name())
        if key in duplicate_class_method_checker:
            duplicate_class_method_checker[key] = class_method_object
        else:
            raise ValueError(
                f"Cannot call method '{class_method_object.get_name()}' of "
                f"class '{class_object_name}'! The method or class is not defined in Class Diagram!"
            )
    return duplicate_class_method_checker


def create_django_project(project_name: str, zipfile_path: str) -> list[str]:
    if not is_valid_python_identifier(project_name):
        raise ValueError(
            f"Project name must not contain whitespace or number! Got: '{project_name}'"
        )

    # write django project template to a dictionary
    files = render_project_django_template(
        os.path.join("app", "templates", "django_project"),
        {"project_name": project_name},
    )
    with zipfile.ZipFile(zipfile_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for name, file in files.items():
            arcname = name if name == "manage.py" else f"{project_name}/{name}"
            zipf.writestr(
                arcname, file()
            )  # file is a lambda function that returns rendered template as str
    return files


def validate_django_app(project_name: str, app_name: str, zipfile_path: str):
    if not is_valid_python_identifier(app_name):
        raise ValueError(f"App name must not contain whitespace! Got: '{app_name}'")
    if not is_valid_python_identifier(project_name):
        raise ValueError(
            f"Project name must not contain whitespace! Got: '{project_name}'"
        )
    if not os.path.exists(zipfile_path):
        raise FileNotFoundError(f"File {zipfile_path} does not exist")


def create_django_app(
    project_name: str,
    app_name: str,
    zipfile_path: str,
    models: str = None,
    views: str = None,
) -> list[str]:
    file_names = []

    validate_django_app(project_name, app_name, zipfile_path)

    with zipfile.ZipFile(zipfile_path, "a", zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir("app/templates/django_app"):
            # file that use jinja2 template
            if file == "apps.py.j2":
                template = render_template(
                    "django_app/apps.py.j2",
                    {"app_name": app_name},  # This is where the app name is passed
                )
                zipf.writestr(f"{app_name}/apps.py", template)
                file_names.append("apps.py")
            else:  # file that use txt file
                """
                Check if the current file is models.txt and if yes, render based on
                the parsed value in the parameter 'models'
                """
                if file == "models.txt" and models is not None:
                    zipf.writestr(f"{app_name}/models.py", models)

                # Check if the current file is views.txt and if yes, render based on
                # the parsed value in the parameter 'views'

                elif file == "views.txt" and views is not None:
                    zipf.writestr(f"{app_name}/views.py", views)

                elif file == "__init__.txt":
                    zipf.writestr(f"{app_name}/migrations/__init__.py", "")
                    zipf.writestr(f"{app_name}/__init__.py", "")
                else:
                    with open(os.path.join(BASE_STATIC_TEMPLATES_DIR, file), "r") as f:
                        content = f.read()
                        file_name = file.replace(".txt", ".py")
                        zipf.writestr(f"{app_name}/{file_name}", content)
            file_names.append(file)
    return file_names


def generate_file_to_be_downloaded(
    project_name: str,
    models: str,
    views: str,
    file_elements: tuple[ModelsElements, RequirementsElements, UrlsElement],
    zipfile_path: str,
) -> list[str]:
    """
    Function to generate the file to be downloaded. This function will create a zip file
    with the name of the project and add all the files to it.
    """
    app_name = "main"
    create_django_project(project_name, zipfile_path)
    create_django_app(project_name, app_name, zipfile_path, models, views)

    with zipfile.ZipFile(zipfile_path, "a", zipfile.ZIP_DEFLATED) as zipf:
        # requirements.txt
        zipf.writestr(
            "requirements.txt",
            file_elements[1].print_django_style(),
        )
        # urls.py
        zipf.writestr(
            f"{app_name}/urls.py",
            file_elements[2].print_django_style(),
        )
        # script files
        zipf.write(
            "app/templates/scripts/run.sh.txt",
            arcname="run.sh",
        )
        zipf.write(
            "app/templates/scripts/run.bat.txt",
            arcname="run.bat",
        )
        # write frontend files to zip

        # CREATE
        writer_models = file_elements[0]
        create_pages = generate_html_create_pages_django(writer_models)
        for name, page in get_names_from_classes(writer_models, create_pages).items():
            file_name = f"create_{name.lower()}.html"
            zipf.writestr(
                f"{app_name}/templates/{file_name}",
                data=page,
            )

        # CREATE FORMS
        forms_create = generate_forms_create_page_django(writer_models)
        zipf.writestr(
            f"{app_name}/forms.py",
            data=forms_create,
        )
        # READ
        read_pages = generate_html_read_pages_django(writer_models)
        for name, page in get_names_from_classes(writer_models, read_pages).items():
            file_name = f"{name.lower()}_list.html"
            zipf.writestr(
                f"{app_name}/templates/{file_name}",
                data=page,
            )

        # UPDATE
        edit_pages = generate_html_edit_pages_django(writer_models)
        for name, page in get_names_from_classes(writer_models, edit_pages).items():
            file_name = f"edit_{name.lower()}.html"
            zipf.writestr(
                f"{app_name}/templates/{file_name}",
                data=page,
            )

        # landing page
        landing_page = generate_landing_page_html()
        zipf.writestr(f"{app_name}/templates/landing_page.html", data=landing_page)

        # base.html
        zipf.write(
            "app/templates/base.html.txt",
            arcname="templates/base.html",
        )

        # Template tags
        zipf.writestr("main/templatetags/__init__.py", "")

        zipf.write(
            "app/templates/templatetags/filter_tag.txt",
            arcname="main/templatetags/filter_tag.py",
        )

        return zipf.namelist()


def get_names_from_classes(
    writer_models: ModelsElements, pages: list[str]
) -> dict[str, str]:
    """
    Function to get the names of the classes and the pages from the writer_models
    """
    classes_dict = {}
    for page, class_obj in (
        (page, class_obj)
        for page in pages
        for class_obj in writer_models.get_classes()
        if class_obj.get_name() in page
    ):
        classes_dict[class_obj.get_name()] = page

    return classes_dict


def process_parsed_class(
    classes: list[ClassObject],
    duplicate_checker: DuplicateChecker,
):
    for model_class in classes:
        for method in model_class.get_methods():
            duplicate_checker[(model_class.get_name(), method.get_name())] = method


def fetch_data(_filenames: list[str], contents: list[list[str]]) -> DataResult:
    """
    This is the logic from convert() method to process the requested
    files. To use this method, pass the request.filename and request.content
    to the parameter of the method fetch_data()
    """
    response_content_models = StringIO()
    response_content_views = StringIO()
    duplicate_class_method_checker: DuplicateChecker = {}

    writer_models = ModelsElements("models.py")
    writer_views = ViewsElements("views.py")

    classes = []
    for content in contents:
        json_content = json.loads(content[0])
        diagram_type = json_content.get("diagram", None)

        if diagram_type is None:
            raise ValueError("Diagram type not found on .jet file")

        if diagram_type == "ClassDiagram":
            with parse_latency.labels(diagram="UML class").time():
                classes = writer_models.parse(json_content)

                process_parsed_class(classes, duplicate_class_method_checker)

        elif diagram_type == "SequenceDiagram":
            with parse_latency.labels(diagram="UML sequence").time():
                seq_parser = ParseJsonToObjectSeq()
                seq_parser.set_json(content[0])
                seq_parser.parse()
                seq_parser.parse_return_edge()

                controller_method_objects = seq_parser.get_controller_method()
                class_objects = seq_parser.get_class_objects()

                for controller_method_object in controller_method_objects:
                    writer_views.add_controller_method(controller_method_object)

                for class_object in class_objects:
                    duplicate_class_method_checker = check_duplicate(
                        class_objects, class_object, duplicate_class_method_checker
                    )

        else:
            raise ValueError(
                "Unknown diagram type. Diagram type must be ClassDiagram or SequenceDiagram! "
                f"Got '{diagram_type}'"
            )

    for class_method_object in duplicate_class_method_checker.values():
        writer_views.add_class_method(class_method_object)

    # Render the base import
    response_content_views.write(render_template("base_views.py.j2"))

    response_content_views.write("\n\n")

    # Render the UML Diagrams method
    response_content_views.write(writer_views.print_django_style())
    response_content_models.write(writer_models.print_django_style())

    # Render the landing page
    if classes:
        response_content_views.write(generate_landing_page_views(classes))
    response_content_views.write("\n")

    # Render the create views
    response_content_views.write(generate_create_page_views(writer_models))

    # Render the read views
    response_content_views.write(generate_read_page_views(writer_models))

    # Render the delete views
    response_content_views.write(generate_delete_page_views(writer_models))

    # Render the edit views
    response_content_views.write(generate_edit_page_views(writer_models))

    return {
        "models": response_content_models.getvalue(),
        "views": response_content_views.getvalue(),
        "model_element": writer_models,
        "views_element": writer_views,
    }


async def initialize_springboot_zip(project_name: str, group_id: str) -> str:
    params = {
        "javaVersion": "21",
        "artifactId": project_name.lower(),
        "groupId": group_id,
        "name": project_name,
        "packaging": "jar",
        "type": "gradle-project-kotlin",
        "dependencies": SPRING_DEPENDENCIES,
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(SPRING_SERVICE_URL + "/starter.zip", params=params)

        if resp.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="Unknown error occured. Initializr service might be down.",
            )

        content_type = resp.headers["content-type"]
        if content_type != "application/zip":
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected content type from server: {content_type}.",
            )

        content = resp.content
        if len(content) == 0:
            raise HTTPException(
                status_code=500, detail="Failed to create zip, please try again later."
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=503,
            detail="Initializr service timed out. Please try again later.",
        )

    except httpx.NetworkError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Initializr service. Service might be down.",
        )

    async with anyio.NamedTemporaryFile(suffix=".zip", delete=False) as f:
        await f.write(content)
        return f.name
