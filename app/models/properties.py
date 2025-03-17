from __future__ import annotations

from copy import deepcopy
from typing import Optional

from app.utils import is_valid_python_identifier


class TypeObject:
    """
    Represents a Datatype

    This class is not framework specific. Instead, it contains methods which return a string
    representation of the datatype according to a specific framework."""

    def __init__(self):
        self.__name = ""

    def set_name(self, name: str):
        self.__name = name

    def to_models_code(self) -> str:
        return self.__name.title()

    def get_name(self) -> str:
        return self.__name

    def __copy__(self) -> TypeObject:
        copy = TypeObject()
        copy.set_name(self.__name)
        return copy

    def __deepcopy__(self, _) -> TypeObject:
        return self.__copy__()

    def __eq__(self, other: TypeObject) -> TypeObject:
        return self.__name == other.__name


class FieldObject:
    """
    Represents a field from a class.

    The FieldObject class is not framework specific. Instead, it contains methods which return a
    string representation of the datatype according to a specific framework."
    """

    def __init__(self):
        self.__name: str = ""
        self.__type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return f"FieldObject:\n\tname: {self.__name}\n\ttype: {self.__type}"

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: TypeObject):
        self.__type = type

    def to_models_code(self) -> str:
        type_mapping = {
            "boolean": "models.BooleanField()",
            "String": "models.CharField(max_length=255)",
            "integer": "models.IntegerField()",
            "float": "models.FloatField()",
            "double": "models.FloatField()",
            "Date": "models.DateField()",
            "DateTime": "models.DateTimeField()",
            "Time": "models.TimeField()",
            "Text": "models.TextField()",
            "Email": "models.EmailField()",
            "URL": "models.URLField()",
            "UUID": "models.UUIDField()",
            "Decimal": "models.DecimalField(max_digits=10, decimal_places=2)",
        }

        field_type = self.__type.to_models_code().lower()

        for key, value in type_mapping.items():
            if key.lower() in field_type:
                return f"{self.__name} = {value}"

        return f"{self.__name} = models.CharField(max_length=255)"  # Default fallback


class ParameterObject:
    """
    Represents parameter of a method definition.

    This class is not framework specific. Instead, it contains methods which return a
    string representation of the datatype according to a specific framework."
    """

    def __init__(self):
        self.__name: str = ""
        self.__type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return f"ParameterObject:\n\tname: {self.__name}\n\ttype: {self.__type}"

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: TypeObject):
        self.__type = type

    def to_views_code(self) -> str:
        if self.__name is None or not is_valid_python_identifier(self.__name):
            raise ValueError(f"Invalid param name: {self.__name}")

        res = self.__name
        if self.__type is not None:
            param_type = self.__type.get_name()
            if not is_valid_python_identifier(param_type):
                raise ValueError(f"Invalid param type: {param_type}")

            res += f": {param_type}"

        return res

    def get_name(self) -> str:
        return self.__name

    def __copy__(self) -> ParameterObject:
        copy = ParameterObject()
        copy.set_name(self.__name)
        copy.set_type(self.__type)
        return copy

    def __deepcopy__(self, _) -> ParameterObject:
        copy = ParameterObject()
        copy.set_name(self.__name)
        copy.set_type(deepcopy(self.__type))
        return copy

    def __eq__(self, other: ParameterObject) -> bool:
        return self.__name == other.__name and self.__type == other.__type
