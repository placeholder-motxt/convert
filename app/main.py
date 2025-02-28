from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from starlette.background import BackgroundTasks
from app.utils import remove_file
from app.model import DownloadRequest
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI World!"}

@app.post("/download/")
async def download_file(request : DownloadRequest, background_tasks: BackgroundTasks):
    file = request.filename+".py"

    if '/' in request.filename or '\\' in request.filename:
        raise HTTPException(status_code=400, detail="/ not allowed")

    if os.path.exists(file):
        raise HTTPException(status_code=400, detail="The file already exists.")

    with open(file, "w") as f:
        f.write(request.content)

    response = FileResponse(path=file, filename=file, media_type='file')

    background_tasks.add_task(remove_file, file)

    return response