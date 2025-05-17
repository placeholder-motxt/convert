from typing import Literal, Optional, TypedDict

from pydantic import BaseModel, Field

from app.models.elements import ModelsElements, ViewsElements
from app.models.methods import ClassMethodObject

Style = Literal["classic", "dark", "minimalist", "modern", "vibrant"]
DuplicateChecker = dict[tuple[str, str], ClassMethodObject]


class DataResult(TypedDict):
    models: str
    views: str
    model_element: ModelsElements
    views_element: ViewsElements


class ConvertRequest(BaseModel):
    filename: list[str] = Field(min_length=1)
    content: list[list[str]] = Field(min_length=1)
    project_name: str = Field(min_length=1)
    project_type: Literal["django", "spring"] = Field(min_length=1, default="django")
    group_id: Optional[str] = Field(min_length=1, default="com.example")
    style_theme: Style = Field(default="modern")


class DownloadRequest(BaseModel):
    filename: str = Field(min_length=3)
    content: str
    type: str = ""
