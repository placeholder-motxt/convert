import json
import os
import shutil
import zipfile
from contextlib import asynccontextmanager
from io import StringIO

import anyio
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.background import BackgroundTasks

from app.config import APP_CONFIG
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
from app.model import ConvertRequest, DownloadRequest
from app.models.elements import (
    ClassObject,
    ModelsElements,
    RequirementsElements,
    UrlsElement,
    ViewsElements,
)
from app.models.methods import ClassMethodObject
from app.parse_json_to_object_seq import ParseJsonToObjectSeq
from app.utils import (
    is_valid_python_identifier,
    logger,
    remove_file,
    render_project_django_template,
    render_template,
)


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    instrumentator.expose(app)
    yield


app = FastAPI(**APP_CONFIG, lifespan=lifespan)
instrumentator = Instrumentator().instrument(app)


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, FastAPI World!"}


async def download_file(request: DownloadRequest) -> FileResponse:
    file = request.filename + request.type + ".py"

    if "/" in request.filename or "\\" in request.filename:
        logger.warning(f"Bad filename: {request.filename}")
        raise HTTPException(status_code=400, detail="/ not allowed in file name")

    if os.path.exists(file):
        logger.warning(f"File already exists: {file}")
        # TODO: Add to metrics so we can know how many request actually face this problem
        raise HTTPException(status_code=400, detail="Please try again later")

    async with await anyio.open_file(file, "w") as f:
        await f.write(request.content)

    logger.info(f"Finished writing: {file}")
    return file


@app.post("/convert")
async def convert(
    request: ConvertRequest,
    background_tasks: BackgroundTasks,
) -> Response:
    if len(request.filename) != len(request.content):
        raise HTTPException(
            status_code=400, detail="number of Filename and Content is incosistent"
        )

    try:
        fetched = fetch_data(request.filename, request.content)
        response_content_models = fetched["models"]
        response_content_views = fetched["views"]
        writer_models = fetched["model_element"]
        writer_requirements = RequirementsElements()

        writer_url = UrlsElement()
        writer_url.set_classes(writer_models.get_classes())

        await download_file(
            request=DownloadRequest(
                filename=request.filename[0],
                content=render_model(fetched),
                type="_models",
            ),
        )

        await download_file(
            request=DownloadRequest(
                filename=request.filename[0],
                content=render_views(fetched),
                type="_views",
            ),
        )

        project_name = request.project_name

        await writer_requirements.write_to_file("./app")
        await writer_url.write_to_file("./app")
        generate_file_to_be_downloaded(
            project_name=project_name,
            models=response_content_models,
            views=response_content_views,
            writer_models=writer_models,
        )
        files = [
            f"{project_name}_models.py",
            f"{project_name}_views.py",
            os.path.join("app", "requirements.txt"),
            os.path.join("app", "urls.py"),
            f"{request.filename[0]}_models.py",
            f"{request.filename[0]}_views.py",
        ]
        if os.path.exists(f"project_{project_name}"):
            shutil.rmtree(f"project_{project_name}")
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        background_tasks.add_task(remove_file, f"{project_name}.zip")

        return FileResponse(
            path=project_name + ".zip",
            filename=f"{project_name}.zip",
            media_type="application/zip",
        )

    except ValueError as ex:
        ex_str = str(ex)
        logger.warning(
            "Error occurred at parsing: " + ex_str.replace("\n", " "), exc_info=True
        )
        raise HTTPException(status_code=422, detail=str(ex))


def check_duplicate(
    class_objects: dict[str, ClassObject],
    class_object_name: str,
    duplicate_class_method_checker: dict[tuple[str, str], ClassMethodObject],
) -> dict[tuple[str, str], ClassMethodObject]:
    class_object = class_objects.get(class_object_name, None)
    if not class_object:
        return duplicate_class_method_checker
    for class_method_object in class_objects[class_object_name].get_methods():
        if (
            class_object_name,
            class_method_object.get_name(),
        ) in duplicate_class_method_checker:
            duplicate_class_method_checker[
                (class_object_name, class_method_object.get_name())
            ] = class_method_object
        else:
            raise ValueError(
                f"Cannot call class '{class_object_name}' objects not defined in Class Diagram!"
            )
    return duplicate_class_method_checker


def create_django_project(project_name: str) -> list[str]:
    files = []
    if not is_valid_python_identifier(project_name):
        raise ValueError("Project name must not contain whitespace or number!")
    zipfile_path = f"{project_name}.zip"
    if os.path.exists(zipfile_path):
        raise FileExistsError(f"File {zipfile_path} already exists")
    zipf = zipfile.ZipFile(zipfile_path, "w")
    # write django project template to a folder
    files = render_project_django_template(
        os.path.join("app", "templates", "django_project"),
        {"project_name": project_name},
    )

    # write folder to zip
    root = os.path.abspath(f"project_{project_name}")
    for file in files:
        file_path = os.path.join(root, file)
        if file == "manage.py":
            zipf.write(file_path, arcname=f"{file}")
        else:
            zipf.write(file_path, arcname=f"{project_name}/{file}")
    zipf.close()
    return files


def validate_django_app(project_name: str, app_name: str):
    if not is_valid_python_identifier(app_name):
        raise ValueError("App name must not contain whitespace!")
    if not is_valid_python_identifier(project_name):
        raise ValueError("Project name must not contain whitespace!")
    if not os.path.exists(f"{project_name}.zip"):
        raise FileNotFoundError(f"File {project_name}.zip does not exist")


def create_django_app(
    project_name: str, app_name: str, models: str = None, views: str = None
) -> list[str]:
    file_names = []

    validate_django_app(project_name, app_name)

    with zipfile.ZipFile(f"{project_name}.zip", "a") as zipf:
        for file in os.listdir("app/templates/django_app"):
            # file that use jinja2 template
            if file == "apps.py.j2":
                file_name = file.replace(".j2", "")
                template = render_template(
                    f"django_app/{file}",
                    {"app_name": app_name},  # This is where the app name is passed
                )
                zipf.writestr(f"{app_name}/{file_name}", template)
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
                    with open(
                        os.path.join("app", "templates", "django_app", file), "r"
                    ) as f:
                        content = f.read()
                        file_name = file.replace(".txt", ".py")
                        zipf.writestr(f"{app_name}/{file_name}", content)
            file_names.append(file)
    return file_names


def generate_file_to_be_downloaded(
    project_name: str,
    models: str,
    views: str,
    writer_models: ModelsElements,
) -> list[str]:
    """
    Function to generate the file to be downloaded. This function will create a zip file
    with the name of the project and add all the files to it.
    """
    # TODO: make app_name dynamic in the future
    if os.path.exists(f"project_{project_name}"):
        shutil.rmtree(f"project_{project_name}", ignore_errors=True)
    if os.path.exists(f"{project_name}.zip"):
        os.remove(f"{project_name}.zip")
    app_name = "main"
    create_django_project(project_name)
    create_django_app(project_name, app_name, models, views)

    with zipfile.ZipFile(f"{project_name}.zip", "a") as zipf:
        # requirements.txt
        if not os.path.exists("app/requirements.txt"):
            raise FileNotFoundError("File requirements.txt does not exist")
        zipf.write(
            os.path.join("app", "requirements.txt"),
            arcname="requirements.txt",
        )
        # urls.py
        if not os.path.exists("app/urls.py"):
            raise FileNotFoundError("File urls.py does not exist")
        zipf.write(
            os.path.join("app", "urls.py"),
            arcname=f"{app_name}/urls.py",
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
        create_pages = generate_html_create_pages_django(writer_models)
        for i in range(len(create_pages)):
            if writer_models.get_classes()[i].get_name() in create_pages[i]:
                page = create_pages[i]
                name = (
                    f"create_{writer_models.get_classes()[i].get_name().lower()}.html"
                )
                zipf.writestr(
                    f"{app_name}/templates/{name}",
                    data=page,
                )
        # CREATE FORMS
        forms_create = generate_forms_create_page_django(models_elements=writer_models)
        zipf.writestr(
            f"{app_name}/forms.py",
            data=forms_create,
        )
        # READ
        read_page = generate_html_read_pages_django(models_elements=writer_models)
        for i in range(len(read_page)):
            if writer_models.get_classes()[i].get_name() in read_page[i]:
                page = read_page[i]
                name = f"{writer_models.get_classes()[i].get_name().lower()}_list.html"
                zipf.writestr(
                    f"{app_name}/templates/{name}",
                    data=page,
                )

        # UPDATE
        edit_page = generate_html_edit_pages_django(models_elements=writer_models)
        for i in range(len(edit_page)):
            for class_obj in writer_models.get_classes():
                if class_obj.get_name() in edit_page[i]:
                    page = edit_page[i]
                    name = f"edit_{class_obj.get_name().lower()}.html"
                    zipf.writestr(
                        f"{app_name}/templates/{name}",
                        data=page,
                    )

        # landing page
        landing_page = generate_landing_page_html()
        zipf.writestr(f"{app_name}/templates/landing_page.html", data=landing_page)
        # base.html
        zipf.write(
            os.path.join("app", "templates", "base.html.txt"),
            arcname="templates/base.html",
        )
        files = zipf.namelist()
    return files


def process_parsed_class(
    classes: list,
    duplicate_checker: dict[tuple[str, str], ClassMethodObject],
):
    for model_class in classes:
        for method in model_class.get_methods():
            duplicate_checker[(model_class.get_name(), method.get_name())] = method


def fetch_data(filename: list[str], content: list[list[str]]) -> dict[str]:
    """
    This is the logic from convert() method to process the requested
    files. To use this method, pass the request.filename and request.content
    to the parameter of the method fetch_data()
    """
    response_content_models = StringIO()
    response_content_views = StringIO()
    duplicate_class_method_checker: dict[tuple[str, str], ClassMethodObject] = dict()

    writer_models = ModelsElements("models.py")
    writer_views = ViewsElements("views.py")

    for file_name, content in zip(filename, content):
        json_content = json.loads(content[0])

        if (
            json_content["diagram"] is not None
            and json_content["diagram"] == "ClassDiagram"
        ):
            classes = writer_models.parse(json_content)

            process_parsed_class(classes, duplicate_class_method_checker)

        elif (
            json_content["diagram"] is not None
            and json_content["diagram"] == "SequenceDiagram"
        ):
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

    for class_method_object in duplicate_class_method_checker.values():
        writer_views.add_class_method(class_method_object)

    # Render the base import
    response_content_views.write(render_template("base_views.py.j2", {}))

    response_content_views.write("\n\n")

    # Render the UML Diagrams method
    response_content_views.write(writer_views.print_django_style())
    response_content_models.write(writer_models.print_django_style())

    # Render the landing page
    response_content_views.write(generate_landing_page_views())
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
    }


def render_model(fetched_data: dict[str]) -> str:
    """
    Function to get the models.py content. Must be called before
    create_django_app and pass the return value to the parameter
    in create_django_app
    """
    return fetched_data["models"]


def render_views(fetched_data: dict[str]) -> str:
    """
    Function to get the views.py content. Must be called before
    create_django_app and pass the return value to the parameter
    in create_django_app

    IMPORTANT NOTE!
    The parameter for render_views is list of JSON Content, so in the
    loop for iterating request.content please make an array to store
    all of the Sequence JSON Content and then pass the array to the
    render_views method!
    """
    return fetched_data["views"]


def get_model_element(fetched_data: dict[str]) -> ModelsElements:
    """
    Function to get ModelElements from the fetch_data method. Behavior
    similiar to render_model and render_views
    """
    return fetched_data["model_element"]
