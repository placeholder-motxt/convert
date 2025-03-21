import json
import os
import zipfile
from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.background import BackgroundTasks

from app.config import APP_CONFIG
from app.model import ConvertRequest, DownloadRequest
from app.models.elements import (
    ClassObject,
    ModelsElements,
    ViewsElements,
)
from app.models.methods import ClassMethodObject
from app.parse_json_to_object_seq import ParseJsonToObjectSeq
from app.utils import (
    is_valid_python_identifier,
    remove_file,
    render_project_django_template,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
        raise HTTPException(status_code=400, detail="/ not allowed in file name")

    if os.path.exists(file):
        raise HTTPException(status_code=400, detail="Please try again later")

    async with await anyio.open_file(file, "w") as f:
        await f.write(request.content)
    print("done writing", file)
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
        response_content_models = ""
        response_content_views = ""
        duplicate_class_method_checker: dict[tuple[str, str], ClassMethodObject] = (
            dict()
        )

        writer_models = ModelsElements("models.py")
        writer_views = ViewsElements("views.py")

        # # Uncomment this to write requirements.txt
        # writer_requirements = RequirementsElements('requirements.txt')

        for file_name, content in zip(request.filename, request.content):
            json_content = content[0]
            if isinstance(json_content, str):
                json_content = json.loads(json_content)

            if (
                json_content["diagram"] is not None
                and json_content["diagram"] == "ClassDiagram"
            ):
                classes = writer_models.parse(json_content)

                for model_class in classes:
                    for method in model_class.get_methods():
                        duplicate_class_method_checker[
                            (model_class.get_name(), method.get_name())
                        ] = method
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
        response_content_views += writer_views.print_django_style()
        response_content_models += writer_models.print_django_style()

        await download_file(
            request=DownloadRequest(
                filename=request.filename[0],
                content=response_content_models,
                type="_models",
            ),
        )

        await download_file(
            request=DownloadRequest(
                filename=request.filename[0],
                content=response_content_views,
                type="_views",
            ),
        )

        # # Uncomment this to write requirements.txt
        # await writer_requirements.write_to_file(
        #     "path_to_project_zip"
        # )
        
        # Write previous files into a .zip
        # project_path: list[str]= create_django_project(request.filename[0])
        zip_filename = request.filename[0] + ".zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(request.filename[0] + "_models.py")
            zipf.write(request.filename[0] + "_views.py")

            os.remove(request.filename[0] + "_models.py")
            os.remove(request.filename[0] + "_views.py")

        background_tasks.add_task(remove_file, zip_filename)

        return FileResponse(
            path=request.filename[0] + ".zip",
            filename=f"{request.filename[0]}.zip",
            media_type="application/zip",
        )

    except ValueError as ex:
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
