import json
from typing import TypedDict

from jsonschema import validate

from app.models.diagram import ClassObject
from app.models.methods import (
    ClassMethodCallObject,
    ClassMethodObject,
    ControllerMethodObject,
)
from app.models.properties import ParameterObject


class CallNode(TypedDict):
    id: int
    parent: int
    method: ClassMethodObject | ControllerMethodObject
    caller: int


class ParseJsonToObjectSeq:
    def __init__(self):
        self.__json = None
        self.__class_object: dict[str, ClassObject] = dict()
        self.__controller_method: list[ControllerMethodObject] = []
        self.__call_nodes: dict[str, CallNode] = dict()
        self.__edges: list = []
        self.__implicit_parameter_nodes: dict[str, str | int | list[int]] = dict()

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
            node_id = node["id"]
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

                self.__implicit_parameter_nodes[node_id] = {
                    "id": node_id,
                    "instance_name": instance_name,
                    "class_name": class_name,
                    "children": node["children"],
                }

            elif node_type == "CallNode":
                self.__call_nodes[node_id] = {"id": node_id, "parent": None}

        """
        Assign children's node into their parents
        """
        for node_id, node_info in self.__implicit_parameter_nodes.items():
            for child_id in node_info["children"]:
                if child_id in self.__call_nodes:
                    self.__call_nodes[child_id]["parent"] = node_id

        # Process edges
        edges = self.__json["edges"]

        valid_caller: set[int] = set()
        for edge in edges:
            edge_type = edge.get("type")
            start_id = edge.get("start")
            end_id = edge.get("end")
            label = edge.get("middleLabel", "")

            self.__edges.append(
                {"type": edge_type, "start": start_id, "end": end_id, "label": label}
            )
            valid_caller.add(end_id)

        # Assign edge to classObject

        # method_tracker: dict[int, ClassMethodObject] = {}
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

                method_label = edge["label"].split(" ")
                is_name_setup = False
                duplicate_attribute_checker = dict()

                for value in method_label:
                    if "[" in value or "]" in value:
                        # TODO: Request Method Implementation
                        continue

                    elif is_name_setup:
                        param = value.replace("(", "").replace(")", "").replace(",", "")

                        if param == "":
                            continue

                        if param in duplicate_attribute_checker:
                            raise Exception("Duplicate attribute!")

                        param_object = ParameterObject()
                        param_object.set_name(param)
                        duplicate_attribute_checker[param] = 1
                        method.add_parameter(param_object)

                    else:
                        method.set_name(value)
                        is_name_setup = True

                if class_name == "views":
                    self.__controller_method.append(method)

                elif method not in class_obj.get_methods():
                    class_obj.add_method(method)

        for node_id, call_node in self.__call_nodes.items():
            caller_id = call_node.get("caller", None)
            if caller_id not in valid_caller:
                continue

            caller_method = self.__call_nodes[caller_id]["method"]
            callee_method = call_node["method"]
            call_obj = ClassMethodCallObject()
            call_obj.set_caller(caller_method)
            call_obj.set_method(callee_method)
            caller_method.add_class_method_call(call_obj)
