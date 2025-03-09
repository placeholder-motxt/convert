import json
import os
import zipfile

import anyio
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from app.model import ConvertRequest, DownloadRequest
from app.models.elements import ModelsElements, ViewsElements
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

    for file_name, content in zip(request.filename, request.content):
        json_content = content[0]
        if isinstance(json_content, str):
            json_content = json.loads(json_content)

        if (
            json_content["diagram"] is not None
            and json_content["diagram"] == "ClassDiagram"
        ):
            writer_models = ModelsElements(file_name)
            classes = writer_models.parse(json_content)

            writer_views = ViewsElements(file_name)
            for model_class in classes:
                for method in model_class.get_methods():
                    writer_views.add_class_method(method)

        # TODO: Parse sequence

        # TODO: Validate Class and Sequence consistency

    response_content_models += writer_models.print_django_style()
    response_content_views += writer_views.print_django_style()

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
