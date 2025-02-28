import json
from jsonschema import validate
from app.element_objects import *

class ParseJsonToObjectSeq:
    def __init__(self):
        self.__json = None

    def set_json(self, data):
        try:
            data_json = json.loads(data)
            
            if(self.validate_json(data_json)):
                self.__json = data_json
                return "Success"

            else:
              raise Exception("Given .jet is not valid!")

        except Exception:
            raise Exception("Given .jet is not valid!")

    def validate_json(self, data):
        schema = {
            "type": "object",
            "required": ["diagram", "nodes", "edges", "version"],
            "properties": {
                "diagram": {
                    "type": "string",
                    "enum": ["SequenceDiagram"]
                },
                "nodes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "type"],
                        "properties": {
                            "id": {"type": "integer"},
                            "type": {
                                "type": "string",
                                "enum": ["ImplicitParameterNode", "CallNode"]
                            },
                            "name": {"type": "string"},
                            "children": {"type": "array", "items": {"type": "integer"}},
                            "x": {"type": "integer"},
                            "y": {"type": "integer"}
                        }
                    }
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
                                "enum": ["CallEdge", "ReturnEdge", "ConstructorEdge"]
                            },
                            "middleLabel": {"type": "string"},
                            "signal": {"type": "boolean"}
                        }
                    }
                },
                "version": {
                    "type": "string"
                }
            }
        }
        try:
            validate(instance=data, schema=schema)
            return True
        
        except Exception:
            return False
        
