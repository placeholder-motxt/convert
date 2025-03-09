import os
import zipfile

import anyio
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from app.model import DownloadRequest
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
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
) -> Response:
    writer = ModelsElements(request.filename)
    classes = writer.parse(request.content)
    response_content = writer.print_django_style()

    await download_file(
        request=DownloadRequest(
            filename=request.filename, content=response_content, type="_models"
        ),
    )

    writer = ViewsElements(request.filename)
    for model_class in classes:
        for method in model_class.get_methods():
            writer.add_class_method(method)
    response_content = writer.print_django_style()

    await download_file(
        request=DownloadRequest(
            filename=request.filename, content=response_content, type="_views"
        ),
    )

    zip_filename = request.filename + ".zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.write(request.filename + "_models.py")
        zipf.write(request.filename + "_views.py")

    os.remove(request.filename + "_models.py")
    os.remove(request.filename + "_views.py")

    background_tasks.add_task(remove_file, zip_filename)

    return FileResponse(
        path=request.filename + ".zip",
        filename=f"{request.filename}.zip",
        media_type="application/zip",
    )
