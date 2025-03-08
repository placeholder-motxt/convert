import json
import re
from typing import TypedDict

from jsonschema import validate

from app.models.diagram import ClassObject
from app.models.methods import (
    ClassMethodCallObject,
    ClassMethodObject,
    ControllerMethodObject,
)
from app.models.properties import ParameterObject

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
        self.__label_pattern: re.Pattern = re.compile(
            r"(\[(?P<cond>.*)\] )?(?P<method_name>.*) "
            r"\((?P<params>.*)?\)( -> (?P<ret_var>.*))?"
        )

    def set_json(self, data: str) -> str | None:
        try:
            data_json = json.loads(data)

            if self.validate_json(data_json):
                self.__json = data_json
                return "Success"

            else:
                raise Exception("Given .jet is not valid!")

        except Exception:
            raise Exception("Given .jet is not valid!")

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

        except Exception:
            return False

    def get_class_objects(self) -> dict[str, ClassObject]:
        return self.__class_object

    def get_controller_method(self) -> list[ControllerMethodObject]:
        return self.__controller_method

    def get_call_nodes(self) -> dict:
        return self.__call_nodes

    def get_edges(self) -> list:
        return self.__edges

    def get_implicit_parameter_nodes(self) -> dict:
        return self.__implicit_parameter_nodes

    def parse(self):
        # duplicate_method_checker = dict()

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
                    raise Exception("Duplicate class name!")

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

        # Process edges
        edges = self.__json["edges"]

        valid_caller: set[int] = set()
        for edge in edges:
            edge_type = edge.get("type")
            start_id = edge.get("start")
            end_id = edge.get("end")
            label = edge.get("middleLabel", "").strip()

            self.__edges.append(
                {"type": edge_type, "start": start_id, "end": end_id, "label": label}
            )
            valid_caller.add(end_id)

        # Assign edge to classObject

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

                match: re.Match[str] | None = self.__label_pattern.match(edge["label"])
                if match is None:
                    raise ValueError(
                        f"Wrong label format: {edge['label']}\n"
                        "Check that the format is in compliance with the guide"
                    )
                condition = match.group("cond")
                method_name = match.group("method_name")
                params = match.group("params")
                ret_var = match.group("ret_var")

                if condition is not None:
                    # TODO: Implement condition checking
                    pass

                if not is_valid_python_identifier(method_name):
                    raise ValueError(f"Invalid method name: {method_name}")
                method.set_name(method_name)

                duplicate_attribute_checker: set[str] = set()
                for param in params.split(","):
                    param = param.strip()
                    if param == "":
                        continue
                    if not is_valid_python_identifier(param):
                        raise ValueError(f"Invalid param name: {param}")
                    if param in duplicate_attribute_checker:
                        raise Exception("Duplicate attribute!")
                    param_obj = ParameterObject()
                    param_obj.set_name(param)
                    method.add_parameter(param_obj)
                    duplicate_attribute_checker.add(param)

                if ret_var is not None:
                    if not is_valid_python_identifier(ret_var):
                        raise ValueError(f"Invalid return variable name: {ret_var}")
                    self.__call_nodes[end_id]["ret_var"] = ret_var

                if class_name == "views":
                    self.__controller_method.append(method)

                elif method not in class_obj.get_methods():
                    class_obj.add_method(method)

        rev_call_tree = {}
        for callee_id, call_node in self.__call_nodes.items():
            caller_id = call_node.get("caller", None)
            if caller_id not in valid_caller:
                continue

            caller_parent = self.__call_nodes[caller_id]["parent"]
            callee_parent = call_node["parent"]
            caller_class = self.__implicit_parameter_nodes[caller_parent]["class_name"]
            callee_class = self.__implicit_parameter_nodes[callee_parent]["class_name"]
            if caller_class == callee_class:
                rev_call_tree[callee_id] = caller_id
                call_depth = self.check_call_depth(rev_call_tree, callee_id)
                if call_depth > self.ALLOWED_SELF_CALL_DEPTH:
                    raise ValueError(
                        "Too deep self calls! "
                        f"The maximum allowed is {self.ALLOWED_SELF_CALL_DEPTH}"
                    )

            caller_method = self.__call_nodes[caller_id]["method"]
            callee_method = call_node["method"]
            ret_var = call_node.get("ret_var", None)
            call_obj = ClassMethodCallObject()
            call_obj.set_caller(caller_method)
            call_obj.set_method(callee_method)
            if ret_var is not None:
                call_obj.set_return_var_name(ret_var)
            caller_method.add_class_method_call(call_obj)

    def check_call_depth(self, rev_call_tree: dict[int, int], callee: int) -> int:
        depth = 0
        caller = rev_call_tree[callee]
        while caller > 0:
            caller = rev_call_tree.get(caller, -1)
            depth += 1
        return depth
