import json
import re

from app.models.diagram import (
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)
from app.models.methods import ClassMethodObject
from app.models.properties import FieldObject, ParameterObject, TypeObject

from .utils import is_valid_python_identifier


class ParseJsonToObjectClass:
    def __init__(self, data: str):
        self.__json = data

        """
        This regex will match anything that starts with + or -
        and then followed by any string imaginable seperated
        with or without space
        """
        self.__public_regex = r"(^[\+\-]) ?(?P<class_name>\w*)"

        if isinstance(data, str):
            try:
                self.__json = json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("Error: Invalid JSON format")
        self.__classes = []

    def check_name(self, name: str) -> bool:
        return is_valid_python_identifier(name)

    def parse_classes(self) -> list:
        data = self.__json

        if "nodes" not in data.keys() or data["nodes"] == "" or data["nodes"] == []:
            raise ValueError(
                "Nodes not found in the json, \nplease make sure the file isn't corrupt"
            )

        # iterate all class in json
        for object in data["nodes"]:
            if object["name"] == "":
                raise ValueError(
                    "Class not found in the json, \n"
                    "please make sure the file isn't corrupt"
                )
            class_obj = ClassObject()

            object_name = object["name"]

            if bool(re.match(self.__public_regex, object_name)):
                if object_name[0] == "+":
                    class_obj.set_is_public(True)
                else:
                    class_obj.set_is_public(False)
                object_name = object_name[1:].strip()
            else:
                class_obj.set_is_public(False)

            if self.check_name(object_name):
                class_obj.set_name(object_name)
            else:
                raise ValueError(
                    "Class name is not valid \n"
                    "please consult the user manual document on how to name classes"
                )

            class_obj.set_id(object["id"])

            if "attributes" in object.keys() and object["attributes"] != "":
                attributes = object["attributes"].split("\n")
            else:
                attributes = []

            # iterate all method in a class
            methods = (
                object["methods"].replace("+", "\n").replace("-", "\n").split("\n")
            )
            for method in methods:
                if method != "":
                    class_method_obj = ClassMethodObject()
                    class_method_name = method.split("(")[0].lstrip("+- ").strip()
                    if ":" in method.split(")")[1]:
                        class_method_rettype_name = (
                            method.split(")")[1].split(":")[1].strip()
                        )
                    else:
                        raise ValueError(
                            "Method return type not found, \n"
                            f"please add a return type for method {method}"
                        )

                    # check if method and method return type name is valid
                    if (
                        self.check_name(class_method_name)
                        and self.check_name(class_method_rettype_name)
                        or bool(re.match(r"List\[.*\]", class_method_rettype_name))
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

                    # iterate all parameter in a method
                    parameters = method.split("(")[1].split(")")[0].split(", ")

                    if parameters != [""]:
                        for parameter in parameters:
                            param_obj = ParameterObject()
                            param_type = TypeObject()
                            param_name = parameter.split(":")[0]
                            param_type_name = parameter.split(":")[1].strip()
                            if self.check_name(param_name) and self.check_name(
                                param_type_name
                            ):
                                param_obj.set_name(param_name)
                                param_type.set_name(param_type_name)
                                param_obj.set_type(param_type)

                            else:
                                raise ValueError(
                                    f"'{param_name}' is not a valid!"
                                    "Parameter name please consult the user "
                                    "manual document on how to name parameters"
                                )

                            class_method_obj.add_parameter(param_obj)

                    class_obj.add_method(class_method_obj)

            if attributes != []:
                for attribute in attributes:
                    if attribute != "":
                        attribute = attribute.lstrip("+- ")

                        attr = FieldObject()
                        attr_type = TypeObject()

                        attr_name = attribute.split(":")[0].strip()
                        attr_type_name = attribute.split(":")[1].strip()

                        if (
                            self.check_name(attr_name)
                            and self.check_name(attr_type_name)
                            or bool(re.match(r"List\[.*\]", attr_type_name))
                        ):
                            attr.set_name(attr_name)
                            attr_type.set_name(attr_type_name)
                            attr.set_type(attr_type)

                            class_obj.add_field(attr)
                        else:
                            raise ValueError(
                                f"Error: attribute name or type is not valid: {attr_name}, "
                                f"{attr_type_name}"
                            )

            self.__classes.append(class_obj)
        return self.__classes

    def parse_relationships(self, classes: list[ClassObject]) -> list[ClassObject]:
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

            ro = None
            if (
                "*" in edge["startLabel"]
                or "." in edge["startLabel"]
                or self.__is_number_greater_than(edge["startLabel"])
            ) and (
                "*" in edge["endLabel"]
                or "." in edge["endLabel"]
                or self.__is_number_greater_than(edge["endLabel"])
            ):
                ro = ManyToManyRelationshipObject()

            elif (
                "*" in edge["startLabel"]
                or "." in edge["startLabel"]
                or self.__is_number_greater_than(edge["startLabel"])
            ) or (
                "*" in edge["endLabel"]
                or "." in edge["endLabel"]
                or self.__is_number_greater_than(edge["endLabel"])
            ):
                ro = ManyToOneRelationshipObject()

                if (
                    "*" in edge["startLabel"]
                    or "." in edge["startLabel"]
                    or self.__is_number_greater_than(edge["startLabel"])
                ):
                    ro.set_source_class_own_amount(edge["startLabel"])
                    ro.set_target_class_own_amount(edge["endLabel"])

                    class_from_id.add_relationship(ro)
                    ro.set_source_class(class_from_id)
                    ro.set_target_class(class_to_id)
                else:
                    ro.set_source_class_own_amount(edge["endLabel"])
                    ro.set_target_class_own_amount(edge["startLabel"])

                    class_to_id.add_relationship(ro)
                    ro.set_source_class(class_to_id)
                    ro.set_target_class(class_from_id)
                continue
            else:
                ro = OneToOneRelationshipObject()

            ro.set_source_class(class_from_id)
            ro.set_target_class(class_to_id)

            ro.set_source_class_own_amount(edge["startLabel"])
            ro.set_target_class_own_amount(edge["endLabel"])
            class_from_id.add_relationship(ro)
        return classes

    def __validate_amount(self, amount_str: str) -> str:
        if not amount_str:
            raise ValueError("Association multiplicity is empty on relation")

        # Kalo bentuknya bukan * atau N..*
        if "*" in amount_str and "*" != amount_str[len(amount_str) - 1]:
            raise ValueError("Invalid use of * in multiplicity on relation")

        # Amount hanya angka
        if amount_str.isnumeric() or amount_str == "*":
            return amount_str

        else:
            # validate minimum and maximum amount
            end_minimum = False
            start_max = False
            has_min_number = False
            titik_count = 0
            for i, ch in enumerate(amount_str):
                if ch.isdigit() and not end_minimum:
                    has_min_number = True
                elif has_min_number and ch == ".":
                    end_minimum = True
                    titik_count += 1
                elif end_minimum and not start_max and ch.isdigit():
                    start_max = True
                elif end_minimum and ch == "*" and i == len(amount_str) - 1:
                    start_max = True
                elif start_max and ch.isdigit():
                    pass
                else:
                    raise ValueError("Invalid multiplicity on relationship")
            if (end_minimum and not start_max) or titik_count != 2:
                raise ValueError("Invalid multiplicity on relationship")

            return amount_str

    def __is_number_greater_than(self, amount_str: str, compared_to: int = 1) -> bool:
        if amount_str.isnumeric():
            return int(amount_str) > compared_to
