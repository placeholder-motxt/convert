from __future__ import annotations

from abc import ABC, abstractmethod
from io import StringIO
from typing import Optional

from app.utils import is_valid_python_identifier


class ClassObject:
    def __init__(self):
        self.__name: str = ""
        self.__parent: Optional[ClassObject] = None
        self.__fields: list[FieldObject] = []
        self.__methods: list[ClassMethodObject] = []
        self.__relationships: list[AbstractRelationshipObject] = []

        self.__id: int


    def to_models_code(self) -> str:
        return (
            f"class {self.__name}"
            + f"({self.__parent.get_name() if self.__parent else 'models.Model'}):"
            + f"\n{self.__get_attributes_to_code()}\n{self.__get_relationships_to_code()}"
            + f"\n{self.__get_methods_to_code()}"
        )
      
    def __str__(self) -> str:
        return (
            f"Class Object:\n\tname: {self.__name}\n\tparent: {self.__parent}"
            f"\n\tfields:{self.__fields}\n\t methods: {self.__methods}"
            f"\n\trelationships: {self.__relationships}"
        )

    def set_name(self, name: str):
        self.__name = name

    def set_parent(self, parent: ClassObject):
        self.__parent = parent

    def add_field(self, field: FieldObject):
        self.__fields.append(field)

    def add_method(self, method: ClassMethodObject):
        self.__methods.append(method)

    def add_relationship(self, relationship: AbstractRelationshipObject):
        self.__relationships.append(relationship)

    def set_id(self, id: int):
        self.__id = id

    def get_name(self) -> str:
        return self.__name

    def __get_attributes_to_code(self) -> str:
        res = ""
        for attribute in self.__fields:
            res += "\t" + attribute.to_models_code() + "\n"
        return res

    def __get_relationships_to_code(self) -> str:
        res = ""
        for relation in self.__relationships:
            res += "\t" + relation.to_models_code() + "\n"
        return res

    def __get_methods_to_code(self) -> str:
        # TODO: Implement this
        return ""


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


class AbstractMethodObject(ABC):
    def __init__(self):
        self.__name: str = ""
        self.__parameters: list[ParameterObject] = []
        self.__return_type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return (
            f"MethodObject:\n\tname: {self.__name}\n\tparameters: {self.__parameters}"
            f"\n\treturn_type: {self.__return_type}"
        )

    def set_name(self, name: str):
        self.__name = name

    def add_parameter(self, parameter: ParameterObject):
        self.__parameters.append(parameter)

    def set_return_type(self, return_type: TypeObject):
        self.__return_type = return_type

    def get_name(self) -> str:
        return self.__name

    def get_parameters(self) -> list[ParameterObject]:
        # TODO: Make immutable if needed
        return self.__parameters

    def get_returnType(self) -> TypeObject:
        # TODO: Make immutable if needed
        return self.__return_type

    def get_name(self) -> str:
        return self.__name

    def get_parameters(self) -> list[ParameterObject]:
        # TODO: Make immutable if needed
        return self.__parameters

class ClassMethodObject(AbstractMethodObject):
    def __init__(self):
        super().__init__()
        self.__calls: list[ClassMethodCallObject] = []

    def add_class_method_call(self, class_method_call: ClassMethodCallObject):
        if class_method_call is None:
            raise Exception("Cannot add None to ClassMethodCallObject!")
        self.__calls.append(class_method_call)

    def to_views_code(self) -> str:
        name = self.get_name()
        if name is None or not is_valid_python_identifier(name):
            raise ValueError(f"Invalid method name: {name}")

        params = ", ".join([param.to_views_code() for param in self.get_parameters()])
        res = f"def {name}({params})"

        ret = self.get_returnType()
        if ret is not None:
            rettype = ret.get_name()
            if not is_valid_python_identifier(rettype):
                raise ValueError(f"Invalid return type: {rettype}")
            res += f" -> {rettype}"
        res += ":\n    # TODO: Auto generated function stub\n"
        res += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        return res


class AbstractRelationshipObject(ABC):
    def __init__(self):
        self.__source_class: Optional[ClassObject] = None
        self.__target_class: Optional[ClassObject] = None
        self.__sourceClassOwnAmount: str = ""
        self.__targetClassOwnAmount: str = ""

    def set_source_class(self, source_class: ClassObject):
        if source_class is None:
            raise Exception("Source Class cannot be SET to be None!")
        self.__source_class = source_class

    def set_target_class(self, target_class: ClassObject):
        if target_class is None:
            raise Exception("Target Class cannot be SET to be None!")
        self.__target_class = target_class

    def setSourceClassOwnAmount(self, amount: str):
        self.__sourceClassOwnAmount = amount

    def setTargetClassOwnAmount(self, amount: str):
        self.__targetClassOwnAmount = amount

    def get_source_class(self) -> ClassObject:
        return self.__source_class

    def get_target_class(self) -> ClassObject:
        return self.__target_class


class TypeObject:
    def __init__(self):
        self.__name = ""

    def set_name(self, name: str):
        self.__name = name

    def to_models_code(self) -> str:
        return self.__name.title()

    def get_name(self) -> str:
        return self.__name


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



class AbstractMethodCallObject(ABC):
    def __init__(self):
        self.__method: AbstractMethodObject = None
        self.__arguments: list[ArgumentObject] = []
        self.__return_var_name: str = ""
        self.__condition = ""

    def __str__(self) -> str:
        return (
            f"MethodCallObject:\n\tmethod: {self.__method}\n\t"
            f"arguments: {self.__arguments}\n\treturn_var_name: {self.__return_var_name}"
        )

    def set_method(self, method: AbstractMethodObject):
        self.__method = method

    def add_argument(self, argument: ArgumentObject):
        self.__arguments.append(argument)

    def set_return_var_name(self, return_var_name: str):
        self.__return_var_name = return_var_name

    def set_condition(self, condition: str):
        self.__condition = condition

    def print_django_style(self) -> str:
        result = StringIO()
        if self.__condition:
            result.write(f"if {self.__condition}:\n\t\t")
        if self.__return_var_name:
            result.write(f"{self.__return_var_name} = ")
        result.write(f"{self.__method.get_name()}(")
        if self.__arguments:
            arguments_str = ", ".join(
                arg.print_django_style() for arg in self.__arguments
            )
            result.write(arguments_str)
        result.write(")")
        return result.getvalue()


class ArgumentObject():
    def __init__(self):
        self.__method_object: Optional[AbstractMethodCallObject] = None
        self.__name: str = ""
        self.__type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return (
            f"ArgumentObject:\n\tmethodObject: \n\t[{self.__method_object}]"
            f"\n\tname: {self.__name}\n\ttype: \n\t[{self.__type}]"
        )

    def set_methodObject(self, methodObject: AbstractMethodCallObject):
        self.__method_object = methodObject

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: TypeObject):
        self.__type = type

    def print_django_style(self) -> str:
        return self.__name


class OneToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()} = "
            + f"models.OneToOneField({self.get_target_class().get_name()},"
            + " on_delete = models.CASCADE)"
        )


class ManyToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()}FK "
            + f"= models.ForeignKey({self.get_target_class().get_name()}, "
            + "on_delete = models.CASCADE)"
        )


class ManyToManyRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"listOf{self.get_target_class().get_name().title()}"
            + f" = models.ManyToManyField({self.get_target_class().get_name()},"
            + " on_delete = models.CASCADE)"
        )


class ControllerMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None

    def set_caller(self, caller: ClassMethodObject):
        self.__caller = caller


class ControllerMethodObject(AbstractMethodObject):
    def __init__(self):
        super().__init__()
        self.__calls: list[AbstractMethodCallObject] = []

    def add_call(self, call_object: AbstractMethodCallObject):
        self.__calls.append(call_object)

    def print_django_style(self) -> str:
        if not self.get_name():
            raise TypeError("method cannot be empty")
        result = StringIO()
        result.write(f"def {self.get_name()}(request")
        for parameter in self.get_parameters():
            result.write(f", {parameter.get_name()}")
        result.write("):\n\t")
        for abstract_method_call_object in self.__calls:
            result.write(abstract_method_call_object.print_django_style())
            result.write("\n\t")
        result.write("\n")
        return result.getvalue()


class ClassMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None

    def set_caller(self, method_object: ClassMethodObject):
        if method_object is None:
            raise Exception("ClassMethodObject cannot be SET to be None!")
        self.__caller = method_object


class FileElements(ABC):
    def __init__(self, file_name: str):
        assert isinstance(file_name, str), "File name must be a string!"
        assert file_name != "", "File name can't be empty!"
        self.__name: str = file_name

    @abstractmethod
    def print_django_style(self) -> str:  # pragma: no cover
        pass


class ModelsElements(FileElements):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__classes: list[ClassObject] = []

    def print_django_style(self) -> str:
        pass  # TODO: PBI 1-7


class ViewsElements(FileElements):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__class_methods: list[ClassMethodObject] = []
        self.__controller_methods: list[ControllerMethodObject] = []

    def print_django_style(self) -> str:
        result = StringIO()

        for class_method_object in self.__class_methods:
            # TODO: PBI-1-7 and PBI 2-9
            pass

        for controller_method_object in self.__controller_methods:
            result.write(controller_method_object.print_django_style())
        return result.getvalue()

    def add_class_method(self, class_method_object: ClassMethodObject):
        self.__class_methods.append(class_method_object)

    def add_controller_method(self, controller_method_object: ControllerMethodObject):
        self.__controller_methods.append(controller_method_object)
