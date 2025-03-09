from pydantic import BaseModel, Field


class DownloadRequest(BaseModel):
    filename: str = Field(min_length=3)
    content: str
    type: str = ""
