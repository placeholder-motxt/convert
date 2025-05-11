import json
import re
from typing import TypedDict

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from app.models.diagram import ClassObject
from app.models.methods import (
    AbstractMethodCallObject,
    AbstractMethodObject,
    ArgumentObject,
    ClassMethodCallObject,
    ClassMethodObject,
    ControllerMethodCallObject,
    ControllerMethodObject,
)
from app.models.properties import ParameterObject, TypeObject

from .utils import is_valid_python_identifier


class CallNode(TypedDict):
    id: int
    parent: int
    method: ClassMethodObject | ControllerMethodObject
    caller: int
    ret_var: str


class ParseJsonToObjectSeq:
    ALLOWED_SELF_CALL_DEPTH = 5

    def __init__(self):
        self.__json = None
        self.__class_object: dict[str, ClassObject] = dict()
        self.__controller_method: list[ControllerMethodObject] = []
        self.__call_nodes: dict[str, CallNode] = dict()
        self.__edges: list = []
        self.__implicit_parameter_nodes: dict[str, str | int | list[int]] = dict()
        self.__method_call: dict[tuple, dict] = dict()
        self.__label_pattern = re.compile(
            r"^(\[(?P<cond>.*)\] )?(?P<method_name>.*?)"
            r"[ ]?\((?P<params>.*)?\)( -> (?P<ret_var>.*))?$"
        )

    def set_json(self, data: str) -> str | None:
        try:
            data_json = json.loads(data)

            if self.validate_json(data_json):
                self.__json = data_json
                return "Success"

            else:
                raise ValueError(
                    "The .sequence.jet is not valid. \n"
                    "Please make sure the file submitted is not corrupt"
                )

        except json.JSONDecodeError:
            raise ValueError(
                "The .sequence.jet is not valid. \n"
                "Please make sure the file submitted is not corrupt"
            )

    def validate_json(self, data: object) -> bool:
        schema = {
            "type": "object",
            "required": ["diagram", "nodes", "edges", "version"],
            "properties": {
                "diagram": {"type": "string", "enum": ["SequenceDiagram"]},
                "nodes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "type"],
                        "properties": {
                            "id": {"type": "integer"},
                            "type": {
                                "type": "string",
                                "enum": ["ImplicitParameterNode", "CallNode"],
                            },
                            "name": {"type": "string"},
                            "children": {"type": "array", "items": {"type": "integer"}},
                            "x": {"type": "integer"},
                            "y": {"type": "integer"},
                        },
                    },
                },
                "edges": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["start", "end", "type"],
                        "properties": {
                            "start": {"type": "integer"},
                            "end": {"type": "integer"},
                            "type": {
                                "type": "string",
                                "enum": ["CallEdge", "ReturnEdge", "ConstructorEdge"],
                            },
                            "middleLabel": {"type": "string"},
                            "signal": {"type": "boolean"},
                        },
                    },
                },
                "version": {"type": "string"},
            },
        }
        try:
            validate(instance=data, schema=schema)
            return True

        except ValidationError:
            return False

    def get_method_call(self) -> dict:  # pragma: no cover
        return self.__method_call

    def get_class_objects(self) -> dict[str, ClassObject]:  # pragma: no cover
        return self.__class_object

    def get_controller_method(self) -> list[ControllerMethodObject]:  # pragma: no cover
        return self.__controller_method

    def get_call_nodes(self) -> dict:  # pragma: no cover
        return self.__call_nodes

    def get_edges(self) -> list:  # pragma: no cover
        return self.__edges

    def get_implicit_parameter_nodes(self) -> dict:  # pragma: no cover
        return self.__implicit_parameter_nodes

    def assign_node_into_classobject(self):
        """
        Assign all nodes into ClassObject and keep the information in a dictionary
        """
        for node in self.__json["nodes"]:
            callee_id = node["id"]
            node_type = node["type"]

            if node_type == "ImplicitParameterNode":
                node_name = node["name"]
                splitted_name = node_name.split(":")
                instance_name = splitted_name[0]
                class_name = splitted_name[1]

                if class_name not in self.__class_object:
                    class_object = ClassObject()
                    class_object.set_name(class_name)
                    self.__class_object[class_name] = class_object

                else:
                    raise ValueError(
                        f"Duplicate class name '{class_name}' on sequence diagram"
                    )

                self.__implicit_parameter_nodes[callee_id] = {
                    "id": callee_id,
                    "instance_name": instance_name,
                    "class_name": class_name,
                    "children": node["children"],
                }

            elif node_type == "CallNode":
                self.__call_nodes[callee_id] = {"id": callee_id, "parent": None}

        """
        Assign children's node into their parents
        """
        for callee_id, node_info in self.__implicit_parameter_nodes.items():
            for child_id in node_info["children"]:
                if child_id in self.__call_nodes:
                    self.__call_nodes[child_id]["parent"] = callee_id

    def process_edge_json(self, valid_caller: set[int]):
        # Process edges
        edges = self.__json["edges"]

        for edge in edges:
            edge_type = edge.get("type")
            start_id = edge.get("start")
            end_id = edge.get("end")
            label = edge.get("middleLabel", "").strip()

            self.__edges.append(
                {"type": edge_type, "start": start_id, "end": end_id, "label": label}
            )
            key_tuple = (start_id, end_id)
            self.__method_call[key_tuple] = {
                "end": end_id,
                "condition": None,
                "method": None,
                "ret_var": None,
                "method_call": None,
            }
            valid_caller.add(end_id)

    def check_for_duplicate_attribute(
        self,
        params: str,
        method: AbstractMethodObject,
        duplicate_attribute_checker: set,
    ):
        for param in params.split(","):
            param = param.strip()
            param = param.replace(" ", "")

            param_type = ""

            if ":" in param:
                data_split = param.split(":")
                param = data_split[0]
                param_type = data_split[1]

            if param == "":
                continue

            if not is_valid_python_identifier(param):
                raise ValueError(
                    f"Invalid param name '{param}' on sequence diagram \n\
please consult the user manual document on how to name parameters"
                )
            if param in duplicate_attribute_checker:
                raise ValueError(
                    f"Duplicate attribute '{param}' on sequence diagram \n\
please remove one of the parameters"
                )

            param_obj = ParameterObject()
            param_obj.set_name(param)
            if param_type != "":
                type_object = TypeObject()
                type_object.set_name(param_type)
                param_obj.set_type(type_object)

            method.add_parameter(param_obj)
            duplicate_attribute_checker.add(param)

    def process_regex_into_object(
        self,
        edge: dict,
        method: AbstractMethodObject,
        start_id: str,
        end_id: str,
        class_name: str,
        class_obj: ClassObject,
    ):
        match: re.Match[str] | None = self.__label_pattern.match(edge["label"])
        if match is None:
            raise ValueError(
                f"Wrong label format '{edge['label']}' on sequence diagram \n\
please consult the user manual document on how to name parameters"
            )
        condition = match.group("cond")
        method_name = match.group("method_name")
        params = match.group("params")
        ret_var = match.group("ret_var")

        if not is_valid_python_identifier(method_name):
            raise ValueError(
                f"Invalid method name '{method_name}' on sequence diagram \n"
                "please consult the user manual document on how to name methods"
            )
        method.set_name(method_name)

        duplicate_attribute_checker: set[str] = set()
        self.check_for_duplicate_attribute(params, method, duplicate_attribute_checker)

        if ret_var is not None:
            #             if not is_valid_python_identifier(ret_var):
            #                 raise ValueError(
            #                     f"Invalid return variable name '{ret_var}' on sequence diagram \n\
            # please consult the user manual document on how to name return variables"
            #                 )
            self.__call_nodes[end_id]["ret_var"] = ret_var

        if class_name == "views":
            self.__controller_method.append(method)

        elif method not in class_obj.get_methods():
            class_obj.add_method(method)

        method_call_dictionary = self.__method_call[(start_id, end_id)]
        if condition is not None and method_call_dictionary["end"] == end_id:
            method_call_dictionary["condition"] = condition
        method_call_dictionary["method"] = method

    def process_edge_into_classobject(self):
        for edge in self.__edges:
            if edge["type"] == "CallEdge":
                start_id = edge["start"]
                end_id = edge["end"]
                parent_id = self.__call_nodes[end_id]["parent"]
                class_name = self.__implicit_parameter_nodes[parent_id]["class_name"]
                class_obj = self.__class_object[class_name]

                if class_name == "views":
                    method = ControllerMethodObject()

                else:
                    method = ClassMethodObject()

                self.__call_nodes[end_id]["method"] = method
                self.__call_nodes[end_id]["caller"] = start_id

                self.process_regex_into_object(
                    edge, method, start_id, end_id, class_name, class_obj
                )

    def process_self_call(
        self, caller_id: str, callee_id: str, rev_call_tree: dict, call_node: CallNode
    ):
        caller_parent = self.__call_nodes[caller_id]["parent"]
        callee_parent = call_node["parent"]
        caller_class = self.__implicit_parameter_nodes[caller_parent]["class_name"]
        callee_class = self.__implicit_parameter_nodes[callee_parent]["class_name"]
        if caller_class == callee_class:
            rev_call_tree[callee_id] = caller_id
            call_depth = self.check_call_depth(rev_call_tree, callee_id)
            if call_depth > self.ALLOWED_SELF_CALL_DEPTH:
                raise ValueError(
                    "Too deep self calls on a sequence diagram! \n"
                    f"The maximum allowed is {self.ALLOWED_SELF_CALL_DEPTH}"
                )

    def add_argument_object(
        self, callee_method: str, call_obj: AbstractMethodCallObject
    ):
        for param in callee_method.get_parameters():
            argument = ArgumentObject()
            argument.set_name(param.get_name())
            argument.set_method_object(call_obj)
            call_obj.add_argument(argument)

    def process_call_obj(
        self,
        caller_method: AbstractMethodObject,
        callee_method: AbstractMethodObject,
        method_call_dictionary: dict,
        callee_id: str,
    ) -> AbstractMethodCallObject:
        if isinstance(caller_method, ControllerMethodObject):
            call_obj = ControllerMethodCallObject()
            if (
                method_call_dictionary["condition"] is not None
                and method_call_dictionary["end"] == callee_id
            ):
                call_obj.set_condition(method_call_dictionary["condition"])

        else:
            call_obj = ClassMethodCallObject()
            if (
                method_call_dictionary["condition"] is not None
                and method_call_dictionary["end"] == callee_id
            ):
                call_obj.set_condition(method_call_dictionary["condition"])

        call_obj.set_caller(caller_method)
        call_obj.set_method(callee_method)
        return call_obj

    def parse(self):
        self.assign_node_into_classobject()

        valid_caller: set[int] = set()
        self.process_edge_json(valid_caller)
        self.process_edge_into_classobject()

        rev_call_tree = {}
        for edge in self.__edges:
            if edge["type"] == "CallEdge":
                callee_id = edge["end"]
                call_node = self.__call_nodes[callee_id]
                caller_id = call_node.get("caller", None)
                if caller_id not in valid_caller:
                    continue

                self.process_self_call(caller_id, callee_id, rev_call_tree, call_node)

                caller_method = self.__call_nodes[caller_id]["method"]
                callee_method = call_node["method"]
                ret_var = call_node.get("ret_var", None)

                method_call_dictionary = self.__method_call[(caller_id, callee_id)]

                call_obj = self.process_call_obj(
                    caller_method, callee_method, method_call_dictionary, callee_id
                )

                method_call_dictionary["method_call"] = call_obj

                self.add_argument_object(callee_method, call_obj)

                if ret_var is not None:
                    ret_var_name, ret_var_type = self.process_return_variable(ret_var)
                    call_obj.set_return_var_name(ret_var_name)
                    call_obj.set_return_var_type(ret_var_type)

                if isinstance(caller_method, ClassMethodObject):
                    caller_method.add_class_method_call(call_obj)
                else:
                    caller_method.add_call(call_obj)

    def process_return_variable(self, ret_var: str) -> tuple[str, TypeObject]:
        name_type_pair = ret_var.split(sep=":")
        if len(name_type_pair) != 2:
            raise ValueError(
                f"Invalid return variable: {ret_var}!"
                "Format must be <returnVariableName>: <returnVariableType>"
                "\nExample: person: String"
            )
        ret_var_name = name_type_pair[0].strip()
        ret_var_type_name = name_type_pair[1].strip()
        if len(ret_var_type_name) < 1:
            raise ValueError(f"Empty return variable type: {ret_var}!")
        ret_var_type = TypeObject()
        ret_var_type.set_name(ret_var_type_name)
        if len(ret_var_name) < 1:
            raise ValueError(f"Empty return variable name: {ret_var}!")
        return ret_var_name, ret_var_type

    def check_call_depth(
        self, rev_call_tree: dict[int, int], callee: int
    ) -> int | float:
        depth = 0
        visited = set()
        caller = rev_call_tree[callee]
        while caller > 0:
            if caller in visited:
                return float("inf")
            visited.add(caller)
            caller = rev_call_tree.get(caller, -1)
            depth += 1
        return depth

    def parse_return_edge(self) -> list:
        return_vars = []
        for edge in (e for e in self.__edges if e["type"] == "ReturnEdge"):
            label = edge["label"].strip()
            if not is_valid_python_identifier(label):
                raise ValueError(
                    f"Return edge label must be a valid variable name! Given '{edge['label']}' \n\
on sequence diagram please consult the user manual document on how to name methods"
                )

            call_tuple = (edge["end"], edge["start"])
            if call_tuple not in self.__method_call:
                raise ValueError(
                    f"Return edge must have a corresponding call edge on sequence diagram\n"
                    f"{edge['end']} -> {edge['start']}"
                )
            method_call_info = self.__method_call[call_tuple]
            if (
                method_call_info["end"] == edge["start"]
                and method_call_info["method_call"]
            ):
                method_call_info["method_call"].set_ret_var(label)
                return_vars.append(label)

        return return_vars
