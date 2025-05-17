from __future__ import annotations

import re
from abc import ABC
from copy import deepcopy
from io import StringIO
from typing import Optional

from app.utils import (
    JAVA_TYPE_MAPPING,
    is_valid_python_identifier,
    render_template,
    to_camel_case,
)

from .properties import ParameterObject, TypeObject

EMPTY_METHOD_ERR_MSG = "method cannot be empty\nplease consult the user manual document"


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
        self.__modifier: str = ""

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

    def set_modifier(self, modifier: str):
        self.__modifier = modifier

    def get_modifier(self) -> str:
        return self.__modifier


class ClassMethodObject(AbstractMethodObject):
    """
    Represents class methods, or methods defined in a particular models class.

    Its counterpart is the ControllerMethodObject class
    """

    PYTHON_TYPE_MAPPING = {
        "boolean": "bool",
        "string": "str",
        "integer": "int",
    }
    LIST_REGEX = re.compile(r"^list\[(?P<list_type>\w*)\]", re.IGNORECASE)

    __class_object_name: Optional[str] = None

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

    def set_class_object_name(self, class_object_name: str):  # pragma: no cover
        self.__class_object_name = class_object_name

    def get_class_object_name(self) -> str:  # pragma: no cover
        return self.__class_object_name

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
            list_match = self.LIST_REGEX.match(rettype)
            if not is_valid_python_identifier(rettype) and list_match is None:
                raise ValueError(
                    f"Invalid return type: '{rettype}'\n "
                    "please consult the user manual document on how to name return variables"
                )
            if rettype != "void":
                if list_match:
                    # Assuming it is already valid when it comes here
                    list_type = list_match.group("list_type")
                    python_type = self.PYTHON_TYPE_MAPPING.get(
                        list_type.lower(), list_type
                    )
                    res.write(f" -> list[{python_type}]")
                else:
                    python_type = self.PYTHON_TYPE_MAPPING.get(rettype.lower(), rettype)
                    res.write(f" -> {python_type}")

        res.write(":")
        for method_call in self.__calls:
            res.write("\n    ")
            res.write(method_call.print_django_style())

        res.write("\n    # TODO: Auto generated function stub\n")
        self.__add_additional_comments(res)
        res.write(
            f"    raise NotImplementedError('{name} function is not yet implemented')\n    pass\n"
        )

        return res.getvalue()

    def __get_method_call_springboot(self) -> list[str]:
        method_call_string = []

        if self.__calls != []:
            for call in self.__calls:
                result = call.print_springboot_style_template()
                arguments = ", ".join(
                    elem["argument_name"] for elem in result["arguments"]
                )

                if "return_var_type" in result:
                    method_call_string.append(
                        (
                            f"{result['return_var_type']} {result['return_var_name']} = "
                            f"{result['method_name']}({arguments});\n"
                        )
                    )
                else:
                    method_call_string.append(
                        f"{result['method_name']}({arguments});\n"
                    )
        return method_call_string

    def to_springboot_code(self) -> str:
        """
        Return Springboot representation of method in the UML Diagram

        This implementation ignore method calls so only supports for Class Diagram
        """
        name = self.get_name()

        if name is None or not is_valid_python_identifier(name):
            raise ValueError(
                f"Invalid method name '{name}'\n"
                "please consult the user manual document on how to name methods"
            )

        return_type_str = "void"
        ret = self.get_return_type()

        if ret is not None:
            rettype = ret.get_name()
            list_match = self.LIST_REGEX.match(rettype)
            if not is_valid_python_identifier(rettype) and list_match is None:
                raise ValueError(
                    f"Invalid return type: '{rettype}'\n "
                    "please consult the user manual document on how to name return variables"
                )

            if rettype != "void":
                if list_match:
                    list_type = list_match.group("list_type")
                    java_type = JAVA_TYPE_MAPPING.get(list_type.lower(), list_type)
                    return_type_str = f"List<{java_type}>"
                else:
                    return_type_str = JAVA_TYPE_MAPPING.get(rettype.lower(), rettype)

        parameters = self.get_parameters()
        param_str_list = [param.to_springboot_code() for param in parameters]

        param_str = ", ".join(param_str_list)

        modifier = self.get_modifier()
        is_default = modifier == ""

        method_call_string = self.__get_method_call_springboot()

        context = {
            "param": param_str,
            "return_type": return_type_str,
            "name": name,
            "modifier": modifier,
            "is_default": is_default,
            "content": method_call_string,
            "contain_call": (method_call_string != []),
        }

        return render_template("springboot/method.java.j2", context)

    def __add_additional_comments(self, sio: StringIO):
        if len(self.__calls):
            return
        sio.write('    """\n')
        sio.write(
            "    This method is empty due to not having any implementation in the "
            "sequence diagram submited.\n"
        )
        sio.write(
            "    You can resubmit the files again with the function implemented\n"
        )
        sio.write("    in the sequence diagram or implement it yourself\n")
        sio.write('    """\n')

    def to_views_code_template(self) -> dict[str]:
        context = {}
        name = self.get_name()
        if name is None or not is_valid_python_identifier(name):
            raise ValueError(
                f"Invalid method name '{name}'\n"
                "please consult the user manual document on how to name methods"
            )
        context["class_name"] = name
        context["method_name"] = name
        context["params"] = [
            param.to_views_code_template() for param in self.get_parameters()
        ]

        context["return_type"] = "void"
        ret = self.get_return_type()
        if ret is not None:
            rettype = ret.get_name()
            list_match = self.LIST_REGEX.match(rettype)
            if not is_valid_python_identifier(rettype) and list_match is None:
                raise ValueError(
                    f"Invalid return type: '{rettype}'\n "
                    "please consult the user manual document on how to name return variables"
                )
            if rettype != "void":
                if list_match:
                    # Assuming it is already valid when it comes here
                    list_type = list_match.group("list_type")
                    python_type = self.PYTHON_TYPE_MAPPING.get(
                        list_type.lower(), list_type
                    )
                    context["return_type"] = f"list[{python_type}]"
                else:
                    python_type = self.PYTHON_TYPE_MAPPING.get(rettype.lower(), rettype)
                    context["return_type"] = python_type

        context["method_calls"] = [
            method_call.print_django_style_template() for method_call in self.__calls
        ]

        return context

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
            raise ValueError(EMPTY_METHOD_ERR_MSG)
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

    def print_django_style_template(self) -> dict[str]:
        if not self.get_name():
            raise ValueError(EMPTY_METHOD_ERR_MSG)
        context = {}
        context["method_name"] = self.get_name()
        context["params"] = [
            param.to_views_code_template() for param in self.get_parameters()
        ]

        context["method_calls"] = [
            method_call.print_django_style_template() for method_call in self.__calls
        ]
        return context

    def print_springboot_style_template(self) -> dict[str]:
        if not self.get_name():
            raise ValueError(EMPTY_METHOD_ERR_MSG)
        context = {}
        context["method_name"] = self.get_name()
        context["params"] = [
            param.to_springboot_code_template() for param in self.get_parameters()
        ]

        context["method_calls"] = [
            method_call.print_springboot_style_template()
            for method_call in self.__calls
        ]
        context["return_var_declaration"] = self.handle_return_var_declaration(
            context["method_calls"]
        )
        if self.get_return_type() is None:
            context["return_type"] = ""
        else:
            context["return_type"] = self.get_return_type().get_name_springboot()
        return context

    def handle_return_var_declaration(self, method_calls: list[dict]) -> list[dict]:
        encountered_return_var_names = set()

        result = []
        for method_call in method_calls:
            return_var_name = method_call.get("return_var_name")

            if (
                return_var_name not in encountered_return_var_names
                and return_var_name is not None
            ):
                return_var_type = method_call.get("return_var_type")
                if return_var_type is None:
                    raise ValueError(
                        "return variable type not assigned when "
                        f"calling {method_call.get('method_name')} in "
                        f"{self.get_name()} method"
                    )
                result.append(method_call)
                encountered_return_var_names.add(return_var_name)

        return result


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
        self.__return_var_type: Optional[TypeObject] = None
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

    def set_return_var_type(self, type_var: TypeObject):
        self.__return_var_type = type_var

    # Method created since set_return_var_name somehow is broken
    def set_ret_var(self, name: str):  # pragma: no cover
        self.__return_var_name = name

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

    def print_django_style_template(self) -> dict[str]:
        context = {}

        if self.__condition:
            context["condition"] = self.__condition
        if self.__return_var_name:
            context["return_var_name"] = self.__return_var_name
        context["method_name"] = self.__method.get_name()
        if isinstance(self, ClassMethodCallObject):
            context["instance_name"] = self.get_instance_name()

        context["arguments"] = []

        if self.__arguments:
            context["arguments"] = [
                arg.print_django_style_template() for arg in self.__arguments
            ]
        return context

    def print_springboot_style_template(self) -> dict[str]:
        context = {}

        if self.__condition:
            context["condition"] = self.__condition
        if self.__return_var_name:
            context["return_var_name"] = self.__return_var_name
            if self.__return_var_type is None:
                context["return_var_type"] = ""
            else:
                context["return_var_type"] = (
                    self.__return_var_type.get_name_springboot()
                )
        context["method_name"] = self.__method.get_name()
        if isinstance(self, ClassMethodCallObject):
            context["instance_name"] = self.get_instance_name()

        context["arguments"] = []

        if self.__arguments:
            context["arguments"] = [
                arg.print_springboot_style_template() for arg in self.__arguments
            ]
        if isinstance(self.__method, ClassMethodObject):
            context["class_name"] = self.__method.get_class_object_name()
            context["class_name_camel"] = to_camel_case(context["class_name"])
        return context


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

    def print_django_style_template(self) -> dict[str]:
        return {"argument_name": self.__name}

    def print_springboot_style_template(self) -> dict[str]:
        return {"argument_name": self.__name}
