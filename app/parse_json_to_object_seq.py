import json

from jsonschema import validate

from app.models.diagram import ClassObject
from app.models.methods import ArgumentObject, ClassMethodCallObject, ClassMethodObject, ControllerMethodCallObject, ControllerMethodObject
from app.models.properties import ParameterObject


class ParseJsonToObjectSeq:
    def __init__(self):
        self.__json = None
        self.__class_object: dict = dict()
        self.__controller_method: list[ControllerMethodObject] = []
        self.__call_nodes: dict = dict()
        self.__edges: list = []
        self.__implicit_parameter_nodes = dict()

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

    def get_controller_method(self) -> list[ControllerMethodObject]:
        return self.__controller_method

    def get_class_object(self) -> list[ClassObject]:
        return self.__class_object

    def parse(self):
        duplicate_method_checker = dict()

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

        for edge in edges:
            edge_type = edge.get("type")
            start_id = edge.get("start")
            end_id = edge.get("end")
            label = edge.get("middleLabel", "")

            self.__edges.append(
                {"type": edge_type, "start": start_id, "end": end_id, "label": label}
            )

        # Assign edge to classObject

        for edge in self.__edges:
            if edge["type"] == "CallEdge":
                end_id = edge["end"]
                parent_id = self.__call_nodes[end_id]["parent"]
                class_name = self.__implicit_parameter_nodes[parent_id]["class_name"]

                if class_name == "views":
                    method = ControllerMethodObject()

                else:
                    method = ClassMethodObject()

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
                        if value in duplicate_method_checker and duplicate_method_checker[value] == class_name:
                            raise Exception("Duplicate method!")

                        method.set_name(value)
                        duplicate_method_checker[value] = class_name
                        is_name_setup = True
                
                if class_name == "views":
                    self.__controller_method.append(method)
                
                else:
                    self.__class_object[class_name].add_method(method)
        
        # Create method caller
        for edge in self.__edges:
            if edge["type"] == "CallEdge":
                end_id = edge["end"]
                parent_id = self.__call_nodes[end_id]["parent"]
                class_name = self.__implicit_parameter_nodes[parent_id]["class_name"]
                
                method_name = None

                method_label = edge["label"].split(" ")
                is_name_setup = False
                duplicate_attribute_checker = dict()

                for value in method_label:
                    if "[" in value or "]" in value:
                        continue

                    elif is_name_setup:
                        continue

                    else:
                        method_name = value
                        is_name_setup = True
                
                method_accessed = None
                if class_name == "views":
                    for method in self.__controller_method:
                        if (method.get_name() == method_name):
                            method_accessed = method
                else:
                    for method in self.__class_object[class_name].get_method():
                        if (method.get_name() == method_name):
                            method_accessed = method
                
                for edge_call in self.__edges:
                    if edge_call["type"] == "CallEdge":
                        edge_start = edge_call["start"]

                        if edge_start == end_id:
                            parent_id = self.__call_nodes[edge_call["end"]]["parent"]
                            class_name_being_called = self.__implicit_parameter_nodes[parent_id]["class_name"]

                            method_controller_label = edge_call["label"].split(" ")
                            method_being_called = None
                            call_object = None
                            method_being_called_name = ""
                            is_name_setup = False
                            duplicate_attribute_checker_call = dict()

                            if (class_name == "views"):
                                call_object = ControllerMethodCallObject()
                                method_accessed.add_call(call_object)
                                call_object.set_caller(method_accessed)
                            
                            else:
                                call_object = ClassMethodCallObject()
                                method_accessed.add_class_method_call(call_object)
                                call_object.set_caller(method_accessed)

                            for value in method_controller_label:
                                if "[" in value or "]" in value:
                                    continue

                                elif is_name_setup:
                                    param = value.replace("(", "").replace(")", "").replace(",", "")

                                    if param == "":
                                        continue

                                    argument_object = ArgumentObject()
                                    argument_object.set_methodObject(call_object)
                                    argument_object.set_name(param)
                                    call_object.add_argument(argument_object)

                                else:
                                    method_being_called_name = value
                                    is_name_setup = True

                            if (class_name_being_called == "views"):
                                for method in self.__controller_method:
                                    if (method.get_name() == method_being_called_name):
                                        method_being_called = method
                            
                            else:
                                for method in self.__class_object[class_name_being_called].get_method():
                                    if (method.get_name() == method_being_called_name):
                                        method_being_called = method

                            call_object.set_method(method_being_called)