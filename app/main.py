import json
import os
import zipfile

import anyio
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from app.model import ConvertRequest, DownloadRequest
from app.models.elements import ClassObject, ModelsElements, ViewsElements
from app.models.methods import ClassMethodObject
from app.parse_json_to_object_seq import ParseJsonToObjectSeq
from app.utils import remove_file

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, FastAPI World!"}


async def download_file(request: DownloadRequest) -> FileResponse:
    file = request.filename + request.type + ".py"

    if "/" in request.filename or "\\" in request.filename:
        raise HTTPException(status_code=400, detail="/ not allowed")

    if os.path.exists(file):
        raise HTTPException(status_code=400, detail="The file already exists.")

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

    response_content_models = ""
    response_content_views = ""
    duplicate_class_method_checker : dict[tuple[str, str], ClassMethodObject] = dict()

    writer_models = ModelsElements("models.py")
    writer_views = ViewsElements("views.py")

    for file_name, content in zip(request.filename, request.content):
        json_content = content[0]
        if isinstance(json_content, str):
            json_content = json.loads(json_content)


        if (
            json_content["diagram"] is not None
            and json_content["diagram"] == "ClassDiagram"
        ):
            print("masuk sini")
            classes = writer_models.parse(json_content)

            for model_class in classes:
                for method in model_class.get_methods():
                    duplicate_class_method_checker[(model_class.get_name(), method.get_name())] = \
                        method
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
                duplicate_class_method_checker = check_duplicate(class_objects,class_object,
                                                                 duplicate_class_method_checker)
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
            filename=request.filename[0], content=response_content_views, type="_views"
        ),
    )

    # Write previous files into a .zip
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

def check_duplicate(class_objects: dict[str, ClassObject],
                     class_object_name: str,
                     duplicate_class_method_checker: dict[tuple[str, str], ClassMethodObject]) -> \
    dict[tuple[str, str], ClassMethodObject]:
    class_object = class_objects.get(class_object_name,None)
    if not class_object:
        return duplicate_class_method_checker
    for class_method_object in class_objects[class_object_name].get_methods():
        if ((class_object_name, class_method_object.get_name()) in
            duplicate_class_method_checker):
            duplicate_class_method_checker \
                [(class_object_name, class_method_object.get_name())] = class_method_object
        else:
            raise ValueError("Cannot call class objects not defined in Class Diagram!")
    return duplicate_class_method_checker
