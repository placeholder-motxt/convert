from app.utils import is_valid_python_identifier


class TypeObject:
    def __init__(self):
        self.__name = ""

    def set_name(self, name: str):
        self.__name = name

    def to_models_code(self) -> str:
        return self.__name.title()

    def get_name(self) -> str:
        return self.__name


class FieldObject:
    def __init__(self):
        self.__name: str = ""
        self.__type: TypeObject = None

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
    def __init__(self):
        self.__name: str = ""
        self.__type: TypeObject = None

    def __str__(self) -> str:
        return f"ParameterObject:\n\tname: {self.__name}\n\ttype: {self.__type}"

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: str):
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
