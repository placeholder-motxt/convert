import json
import re

from app.models.diagram import (
    ClassObject,
)
from app.models.methods import ClassMethodObject
from app.models.properties import FieldObject, ParameterObject, TypeObject
from app.parse_class_pattern.parse_relationship_state import MultiplicityValidator
from app.parse_class_pattern.parse_relationship_strategy import (
    ManyToManyStrategy,
    ManyToOneStrategy,
    OneToOneStrategy,
    RelationshipStrategy,
)

from .utils import is_valid_python_identifier


class ParseJsonToObjectClass:
    # This regex will match anything that starts with + or -
    # and then followed by any string imaginable seperated
    # with or without space
    PUBLIC_REGEX = re.compile(r"^(?P<visibility>[\+\-]) *(?P<class_name>\w*)")

    LIST_TYPE_REGEX = re.compile(r"^List\[\w*\]")

    def __init__(self, data: str):
        self.__json = data

        if isinstance(data, str):
            try:
                self.__json = json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("Error: Invalid JSON format")
        self.__classes = []

    def parse_classes(self) -> list:
        data = self.__json

        if "nodes" not in data.keys() or data["nodes"] == "" or data["nodes"] == []:
            raise ValueError(
                "Nodes not found in the json, \nplease make sure the file isn't corrupt"
            )

        # iterate all class in json
        for object in data["nodes"]:
            class_obj = self.__create_class(object)

            self.__add_methods_to_class(object, class_obj)

            self.__add_attributes_to_class(object, class_obj)

            self.__classes.append(class_obj)

        return self.__classes

    def parse_relationships(
        self, classes: list[ClassObject], bidirectional: bool = False
    ) -> list[ClassObject]:
        edges = self.__json["edges"]

        for edge in edges:
            class_from_id = classes[edge["start"]]
            class_to_id = classes[edge["end"]]

            if "type" in edge.keys() and edge["type"] == "GeneralizationEdge":
                class_from_id.set_parent(class_to_id)
                continue

            try:
                self.__validate_amount(edge["startLabel"])
                self.__validate_amount(edge["endLabel"])
            except ValueError as ex:
                raise ValueError(
                    str(ex) + f" {class_from_id.get_name()} - {class_to_id.get_name()}"
                )

            strategy = self.__determine_strategy(edge)
            strategy.create_relationship(
                edge, class_from_id, class_to_id, bidirectional
            )

        return classes

    def __create_class(self, object: dict) -> ClassObject:
        if object["name"] == "":
            raise ValueError(
                "Class not found in the json, \nplease make sure the file isn't corrupt"
            )
        class_obj = ClassObject()

        object_name = object["name"]

        match = self.PUBLIC_REGEX.match(object_name)
        if match is not None:
            visibility = match.group("visibility")
            if visibility == "+":
                class_obj.set_is_public(True)
            else:
                class_obj.set_is_public(False)
            object_name = match.group("class_name")
        else:
            class_obj.set_is_public(False)

        if self.__check_name(object_name):
            class_obj.set_name(object_name)
        else:
            raise ValueError(
                "Class name is not valid \n"
                "please consult the user manual document on how to name classes"
            )
        class_obj.set_id(object["id"])

        return class_obj

    def __check_name(self, name: str) -> bool:
        return is_valid_python_identifier(name)

    def __add_methods_to_class(self, object: dict, class_obj: ClassObject) -> None:
        # iterate all method in a class
        methods = object["methods"].split("\n")
        for method in methods:
            if method != "":
                class_method_obj = self.__create_method(method)

                # iterate all parameter in a method
                parameters = method.split("(")[1].split(")")[0].split(", ")

                if parameters != [""]:
                    for parameter in parameters:
                        param_obj = self.__create_parameter(parameter)
                        class_method_obj.add_parameter(param_obj)
                class_obj.add_method(class_method_obj)

    def __create_method(self, method: str) -> ClassMethodObject:
        class_method_obj = ClassMethodObject()
        if method[0] == "+":
            class_method_obj.set_modifier("public")
        elif method[0] == "-":
            class_method_obj.set_modifier("private")
        method = method.replace("+", "").replace("-", "")

        class_method_name = method.split("(")[0].lstrip("+- ").strip()
        if ":" in method.split(")")[1]:
            class_method_rettype_name = method.split(")")[1].split(":")[1].strip()
        else:
            raise ValueError(
                "Method return type not found, \n"
                f"please add a return type for method {method}"
            )

        # check if method and method return type name is valid
        if (
            self.__check_name(class_method_name)
            and self.__check_name(class_method_rettype_name)
            or self.LIST_TYPE_REGEX.match(class_method_rettype_name) is not None
        ):
            class_method_obj.set_name(class_method_name)

            class_method_rettype = TypeObject()
            class_method_rettype.set_name(class_method_rettype_name)
            class_method_obj.set_return_type(class_method_rettype)

        else:
            raise ValueError(
                f"'{class_method_name}' or '{class_method_rettype_name}' "
                "is not a valid "
                "method name or method return type name. \n"
                "please consult the user manual document on "
                "how to name methods and their return types"
            )

        return class_method_obj

    def __add_attributes_to_class(
        self, object: dict[str, str], class_obj: ClassObject
    ) -> None:
        if "attributes" in object and object["attributes"] != "":
            attributes = object["attributes"].split("\n")
            for attribute in attributes:
                if attribute != "":
                    attr = self.__create_attribute(attribute)
                    class_obj.add_field(attr)

    def __create_parameter(self, parameter: str) -> ParameterObject:
        param_obj = ParameterObject()
        param_type = TypeObject()
        param_name = parameter.split(":")[0]
        param_type_name = parameter.split(":")[1].strip()
        if self.__check_name(param_name) and self.__check_name(param_type_name):
            param_obj.set_name(param_name)
            param_type.set_name(param_type_name)
            param_obj.set_type(param_type)
        else:
            raise ValueError(
                f"'{param_name}' is not a valid!"
                "Parameter name please consult the user "
                "manual document on how to name parameters"
            )
        return param_obj

    def __create_attribute(self, attribute: str) -> FieldObject:
        attr_object = FieldObject()
        attr_type = TypeObject()

        modifier = attribute.strip(" ")[0]  # check first character

        if modifier == "+":
            attr_object.set_modifier("public")
        elif modifier == "-":
            attr_object.set_modifier("private")
        else:
            raise ValueError(
                f"""First character of class attribute line must be either "+" or "-" !
                Your attribute line: "{attribute}" """
            )
        attribute = attribute.lstrip("+- ")

        attr_name = attribute.split(":")[0].strip()
        attr_type_name = attribute.split(":")[1].strip()

        if (
            self.__check_name(attr_name)
            and self.__check_name(attr_type_name)
            or self.LIST_TYPE_REGEX.match(attr_type_name)
        ):
            attr_object.set_name(attr_name)
            attr_type.set_name(attr_type_name)
            attr_object.set_type(attr_type)

        else:
            raise ValueError(
                f"Error: attribute name or type is not valid: {attr_name}, "
                f"{attr_type_name}"
            )
        return attr_object

    def __determine_strategy(self, edge: dict) -> RelationshipStrategy:
        start_condition = (
            "*" in edge["startLabel"]
            or "." in edge["startLabel"]
            or self.__is_number_greater_than(edge["startLabel"])
        )
        end_condition = (
            "*" in edge["endLabel"]
            or "." in edge["endLabel"]
            or self.__is_number_greater_than(edge["endLabel"])
        )

        if start_condition and end_condition:
            return ManyToManyStrategy()
        elif start_condition or end_condition:
            return ManyToOneStrategy()
        else:
            return OneToOneStrategy()

    def __validate_amount(self, amount_str: str) -> str:
        if not amount_str:
            raise ValueError("Association multiplicity is empty on relation")

        if "*" in amount_str and "*" != amount_str[-1]:
            raise ValueError("Invalid use of * in multiplicity on relation")

        if amount_str.isnumeric() or amount_str == "*":
            return amount_str

        validator = MultiplicityValidator(amount_str)
        validator.validate()

        return amount_str

    def __is_number_greater_than(self, amount_str: str, compared_to: int = 1) -> bool:
        if amount_str.isnumeric():
            return int(amount_str) > compared_to
