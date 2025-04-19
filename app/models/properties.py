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
        if name.lower() == "string":
            name = "str"
        elif name.lower() == "integer":
            name = "int"
        elif name.lower() == "boolean":
            name = "bool"
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

    DJANGO_TYPE_MAPPING = {
        "boolean": "models.BooleanField()",
        "String": "models.CharField(max_length=255)",
        "str": "models.CharField(max_length=255)",
        "int": "models.IntegerField()",
        "bool": "models.BooleanField()",
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

    SPRING_TYPE_MAPPING = {
        "boolean": "boolean",
        "String": "String",
        "str": "String",
        "int": "Integer",
        "bool": "boolean",
        "integer": "Integer",
        "float": "float",
        "double": "double",
        "Date": "LocalDate",
        "DateTime": "LocalDateTime",
        "Time": "LocalTime",
        "Text": "String",
        "Email": "String",
        "URL": "String",
        "UUID": "UUID",
        "Decimal": "BigDecimal",
    }

    def __init__(self):
        self.__name: str = ""
        self.__type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return f"FieldObject:\n\tname: {self.__name}\n\ttype: {self.__type}"

    def get_name(self) -> str:  # pragma: no cover
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: TypeObject):
        self.__type = type

    def to_models_code(self) -> str:
        field_type = self.__type.to_models_code().lower()

        for key, value in self.DJANGO_TYPE_MAPPING.items():
            if key.lower() in field_type:
                return f"{self.__name} = {value}"

        return f"{self.__name} = models.CharField(max_length=255)"  # Default fallback

    def to_models_code_template(self) -> dict[str, str]:
        field_type = self.__type.to_models_code().lower()

        for key, value in self.DJANGO_TYPE_MAPPING.items():
            if key.lower() in field_type:
                return {"name": self.__name, "type": value}

        return {
            "name": self.__name,
            "type": "models.CharField(max_length=255)",
        }  # Default fallback

    def to_springboot_models_template(self) -> str:
        field_type = self.__type.to_models_code().lower()

        for key, value in self.SPRING_TYPE_MAPPING.items():
            if key.lower() in field_type:
                return {"name": self.__name, "type": value}
        return {"name": self.__name, "type": "String"}  # Default fallback


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
            raise ValueError(
                f"Invalid param name '{self.__name}'\n"
                "please consult the user manual document on how to name parameters"
            )

        res = self.__name
        if self.__type is not None:
            param_type = self.__type.get_name()
            if not is_valid_python_identifier(param_type):
                raise ValueError(
                    f"Invalid param type '{param_type}'\n"
                    "please consult the user manual document on how to name parameter types"
                )

            res += f": {param_type}"

        return res

    def to_views_code_template(self) -> dict[str]:
        context = {}
        context["param_name"] = ""
        if self.__name is None or not is_valid_python_identifier(self.__name):
            raise ValueError(
                f"Invalid param name '{self.__name}'\n"
                "please consult the user manual document on how to name parameters"
            )

        context["param_name"] = self.__name
        if self.__type is not None:
            param_type = self.__type.get_name()
            if not is_valid_python_identifier(param_type):
                raise ValueError(
                    f"Invalid param type '{param_type}'\n"
                    "please consult the user manual document on how to name parameter types"
                )
            context["param_type"] = param_type

        return context

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
