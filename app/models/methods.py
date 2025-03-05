from __future__ import annotations

from abc import ABC
from copy import deepcopy
from io import StringIO
from typing import Optional

from app.utils import is_valid_python_identifier

from .properties import ParameterObject, TypeObject


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
        params = []
        for param in self.__parameters:
            params.append(deepcopy(param))
        return params

    def get_return_type(self) -> TypeObject:
        return deepcopy(self.__return_type)


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

        ret = self.get_return_type()
        if ret is not None:
            rettype = ret.get_name()
            if not is_valid_python_identifier(rettype):
                raise ValueError(f"Invalid return type: {rettype}")
            res += f" -> {rettype}"
        res += ":\n    # TODO: Auto generated function stub\n"
        res += (
            f"    raise NotImplementedError('{name} function is not yet implemented')\n"
        )
        return res


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


class ClassMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None

    def set_caller(self, method_object: ClassMethodObject):
        if method_object is None:
            raise Exception("ClassMethodObject cannot be SET to be None!")
        self.__caller = method_object


class ControllerMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None

    def set_caller(self, caller: ClassMethodObject):
        self.__caller = caller


class ArgumentObject:
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
