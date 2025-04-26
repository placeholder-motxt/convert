from typing import Literal, Optional

from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    filename: list[str] = Field(min_length=1)
    content: list[list[str]] = Field(min_length=1)
    project_name: str = Field(min_length=1)
    project_type: Literal["django", "spring"] = Field(min_length=1, default="django")
    group_id: Optional[str] = Field(min_length=1, default="com.example")


class DownloadRequest(BaseModel):
    filename: str = Field(min_length=3)
    content: str
    type: str = ""
