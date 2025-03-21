from __future__ import annotations

import re
from abc import ABC
from copy import deepcopy
from io import StringIO
from typing import Optional

from app.utils import is_valid_python_identifier

from .properties import ParameterObject, TypeObject


class AbstractMethodObject(ABC):
    """
    Represents a method.

    Note: This class DOES NOT represent abstract methods, instead it represents any method.
    The name is AbstractMethodObject to indicate that this class is not to be instanciated.
    """

    def __init__(self):
        self.__name: str = ""
        self.__parameters: list[ParameterObject] = []
        self.__return_type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return (
            f"MethodObject:\n\tname: {self.__name}\n\tparameters: {self.__parameters}"
            f"\n\treturn_type: {self.__return_type}"
        )

    def __repr__(self) -> str:  # pragma: no cover
        return self.__str__()

    def __eq__(self, other: AbstractMethodObject) -> bool:
        return (
            self.__name == other.__name
            and all(
                self_param == other_param
                for self_param, other_param in zip(
                    self.__parameters, other.__parameters
                )
            )
            and self.__return_type == other.__return_type
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
    """
    Represents class methods, or methods defined in a particular models class.

    Its counterpart is the ControllerMethodObject class
    """

    def __init__(self):
        super().__init__()
        self.__calls: list[ClassMethodCallObject] = []

    def __eq__(self, other: ClassMethodObject) -> bool:
        return all(
            s_call == o_call for s_call, o_call in zip(self.__calls, other.__calls)
        ) and super().__eq__(other)

    def add_class_method_call(self, class_method_call: ClassMethodCallObject):
        if class_method_call is None:
            raise ValueError(
                "Cannot add None to ClassMethodCallObject! "
                "please consult the user manual document"
            )
        self.__calls.append(class_method_call)

    def to_views_code(self) -> str:
        """
        Returns Django representation of the class method in string

        Ultimately, the value returned by this method will be written Django's views.py file.

        Example 1:
        name = 'method_name'
        parameter names = no parameters
        return type name = no return type:
        method call names = 'method_call_1', 'method_call_2'

        Output:
        def method_name(request, instance):
            method_call_1(request, instance)
            # TODO: Auto generated function stub
            raise NotImplementedError('method function is not yet implemented')
            pass

        Example 2:
        name = 'method_name'
        parameter names = 'param1', 'param2'
        return type name = 'str'
        method call names = no method call

        Output:
        def method_name(request, instance, param1, param2) -> str:
            # TODO: Auto generated function stub
            raise NotImplementedError('method function is not yet implemented')
            pass
        """
        res = StringIO()
        name = self.get_name()
        if name is None or not is_valid_python_identifier(name):
            raise ValueError(
                f"Invalid method name '{name}'\n"
                "please consult the user manual document on how to name methods"
            )

        params = ", ".join([param.to_views_code() for param in self.get_parameters()])
        res.write(f"def {name}(request, instance_name")
        if params:
            res.write(f", {params})")
        else:
            res.write(")")

        ret = self.get_return_type()
        if ret is not None:
            rettype = ret.get_name()
            if not is_valid_python_identifier(rettype) and not bool(
                re.match(r"list\[.*\]", rettype.lower())
            ):
                raise ValueError(
                    f"Invalid return type: '{rettype}'\n "
                    "please consult the user manual document on how to name return variables"
                )
            res.write(f" -> {rettype}")
        res.write(":")
        for method_call in self.__calls:
            res.write("\n    ")
            res.write(method_call.print_django_style())
        res.write("\n    # TODO: Auto generated function stub\n")
        res.write(
            f"    raise NotImplementedError('{name} function is not yet implemented')\n    pass\n"
        )

        return res.getvalue()

    def get_calls(self) -> list[ClassMethodCallObject]:  # pragma: no cover
        # TODO: Make immutable if needed
        return self.__calls


class ControllerMethodObject(AbstractMethodObject):
    """
    Represents controller methods, or methods not bound to a particular models class.

    Its counterpart is the ClassMethodObject class
    """

    def __init__(self):
        super().__init__()
        self.__calls: list[AbstractMethodCallObject] = []

    def add_call(self, call_object: AbstractMethodCallObject):
        self.__calls.append(call_object)

    def get_call(self) -> list[AbstractMethodCallObject]:
        return self.__calls

    def print_django_style(self) -> str:
        if not self.get_name():
            raise ValueError(
                "method cannot be empty\nplease consult the user manual document"
            )
        result = StringIO()
        result.write(f"def {self.get_name()}(request")
        for parameter in self.get_parameters():
            result.write(f", {parameter.get_name()}")
        result.write("):\n\t")
        for abstract_method_call_object in self.__calls:
            result.write(abstract_method_call_object.print_django_style())
            result.write("\n\t")
        result.write("pass\n\n")
        return result.getvalue()


class AbstractMethodCallObject(ABC):
    """
    Represents a method call, represented in JetUML .sequence.jet files as arrows.

    Note: This class DOES NOT represent calls made to abstract methods. Instead, it represents
    calls to any method.
    The name AbstractMethodCallObject is to indicate that this class is not to be instanciated.
    """

    def __init__(self):
        self.__method: Optional[AbstractMethodObject] = None
        self.__arguments: list[ArgumentObject] = []
        self.__return_var_name: str = ""
        self.__condition = ""

    def __str__(self) -> str:
        return (
            f"MethodCallObject:\n\tmethod: {self.__method}\n\t"
            f"arguments: {self.__arguments}\n\treturn_var_name: {self.__return_var_name}"
            f"\n\tcondition: {self.__condition}"
        )

    def __eq__(self, other: AbstractMethodCallObject) -> str:
        return (
            self.__method == other.__method
            and all(
                s_arg == o_arg
                for s_arg, o_arg in zip(self.__arguments, other.__arguments)
            )
            and self.__return_var_name == other.__return_var_name
            and self.__condition == other.__condition
        )

    def __repr__(self) -> str:  # pragma: no cover
        return self.__str__()

    def set_method(self, method: AbstractMethodObject):
        self.__method = method

    def get_methods(self) -> AbstractMethodObject:
        return self.__method

    def get_arguments(self) -> list[ArgumentObject]:
        return self.__arguments

    def add_argument(self, argument: ArgumentObject):
        self.__arguments.append(argument)

    def set_return_var_name(self, return_var_name: str):
        self.__return_var_name = return_var_name

    def set_condition(self, condition: str):
        self.__condition = condition

    def get_condition(self) -> str:
        return self.__condition

    def get_method(self) -> AbstractMethodObject:  # pragma: no cover
        # TODO: Make immutable if needed
        return self.__method

    def get_return_var_name(self) -> str:  # pragma: no cover
        return self.__return_var_name

    def print_django_style(self) -> str:
        """
        Returns Django representation of the method call in string

        Example 1:
        method name = 'method1'
        argument names = 'arg1', 'arg2'
        return var name = 'return_var1'
        condition = no condition
        method is instance of ClassMethodCallObject with instance name = "instance_name"

        Output:
        return_var1 = method1(request, instance_name, arg1, arg2)

        Example 2:

        method name = 'method2'
        argument names = no arguments
        return var name = no return value
        condition = True
        method is instance of ControllerMethodCallObject with instance name = "instance_name"

        Output:
        if True:
            method2(request)

        """
        result = StringIO()
        if self.__condition:
            result.write(f"if {self.__condition}:\n\t\t")
        if self.__return_var_name:
            result.write(f"{self.__return_var_name} = ")
        result.write(f"{self.__method.get_name()}(request")
        if isinstance(self, ClassMethodCallObject):
            result.write(f", {self.get_instance_name()}")

        if self.__arguments:
            arguments_str = ", " + ", ".join(
                arg.print_django_style() for arg in self.__arguments
            )
            result.write(arguments_str)
        result.write(")")
        return result.getvalue()


class ClassMethodCallObject(AbstractMethodCallObject):
    """Represents a method call of a ClassMethod"""

    def __init__(self):
        super().__init__()
        self.__caller: Optional[ClassMethodObject] = None
        self.__instance_name = ""

    def __eq__(self, other: ClassMethodCallObject) -> bool:
        return self.__caller == other.__caller and super().__eq__(other)

    def set_caller(self, method_object: ClassMethodObject):
        if method_object is None:
            raise ValueError(
                "ClassMethodObject cannot be SET to be None!\n"
                "please consult the user manual document"
            )
        self.__caller = method_object

    def set_instance_name(self, instance_name: str):
        if instance_name == "" or instance_name is None:
            raise ValueError(
                "instance_name cannot be empty!\n"
                "please consult the user manual document"
            )
        self.__instance_name = instance_name

    def get_instance_name(self) -> str:
        return self.__instance_name

    def get_caller(self) -> ClassMethodObject:  # pragma: no cover
        # TODO: Make immutable if needed
        return self.__caller


class ControllerMethodCallObject(AbstractMethodCallObject):
    """Represents a method call of a ControllerMethod"""

    def __init__(self):
        super().__init__()
        self.__caller: Optional[ControllerMethodObject] = None

    def set_caller(self, caller: ControllerMethodObject):
        self.__caller = caller

    def get_caller(self) -> ClassMethodObject:  # pragma: no cover
        # TODO: Make immutable if needed
        return self.__caller


class ArgumentObject:
    """Represents an argument in a method call"""

    def __init__(self):
        self.__method_object: Optional[AbstractMethodCallObject] = None
        self.__name: str = ""
        self.__type: Optional[TypeObject] = None

    def __str__(self) -> str:
        return (
            f"ArgumentObject:\n\tmethodObject: \n\t[{self.__method_object}]"
            f"\n\tname: {self.__name}\n\ttype: \n\t[{self.__type}]"
        )

    def set_method_object(self, method_object: AbstractMethodCallObject):
        self.__method_object = method_object

    def set_name(self, name: str):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_type(self, type: TypeObject):
        self.__type = type

    def print_django_style(self) -> str:
        """Returns Django representation of the argument in string"""
        return self.__name
