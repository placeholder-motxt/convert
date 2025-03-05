import os

import anyio
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from app.model import DownloadRequest
from app.parse_json_to_object_class import ParseJsonToObjectClass
from app.utils import remove_file

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, FastAPI World!"}


@app.post("/download/")
async def download_file(
    request: DownloadRequest, background_tasks: BackgroundTasks
) -> FileResponse:
    file = request.filename + ".py"

    if "/" in request.filename or "\\" in request.filename:
        raise HTTPException(status_code=400, detail="/ not allowed")

    if os.path.exists(file):
        raise HTTPException(status_code=400, detail="The file already exists.")

    async with await anyio.open_file(file, "w") as f:
        await f.write(request.content)

    response = FileResponse(path=file, filename=file, media_type="file")

    background_tasks.add_task(remove_file, file)

    return response


@app.post("/convert")
async def convert(
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
    fastapi_request: Request,
) -> Response:
    parser = ParseJsonToObjectClass(request.content)
    classes = parser.parse_classes()
    parser.parse_relationships(classes)

    # A faster way to build string
    # https://stackoverflow.com/questions/2414667/python-string-class-like-stringbuilder-in-c
    response_content = "".join(
        [model_class.to_models_code() for model_class in classes]
    )
    response_content = response_content.strip()
    response_content += "\n" if len(response_content) != 0 else ""
    async with httpx.AsyncClient(base_url=str(fastapi_request.base_url)) as client:
        response = await client.post(
            "/download/",
            json={"filename": request.filename, "content": response_content},
        )

    return Response(
        content=response.content, media_type=response.headers["content-type"]
    )
