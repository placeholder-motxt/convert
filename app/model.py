from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    filename: list[str] = Field(min_length=1)
    content: list[list[str]] = Field(min_length=1)


class DownloadRequest(BaseModel):
    filename: str = Field(min_length=3)
    content: str
    type: str = ""
