import unittest
from app.parse_json_to_object import ParseJsonToObject
from app.element_objects import *
from unittest.mock import MagicMock
import json


class TestParseJsonToObject(unittest.TestCase):
    def test_parse(self):
        data = """{
            "diagram": "ClassDiagram",
            "nodes": [
                {
                "methods": "",
                "name": "Pengelola",
                "x": 330,
                "y": 10,
                "attributes": "- isAdmin: boolean",
                "id": 0,
                "type": "ClassNode"
                },
                {
                "methods": "+ getBesaranDenda(nama :Type): integer\\n+ getTglPinjam(): Date\\n+ getTglKembali(): Date",
                "name": "Peminjaman",
                "x": 310,
                "y": 270,
                "attributes": "- ID: String\\n- isDikembalikan: boolean\\n- tglPinjam: Date\\n- tglKembali: Date\\n- isLunasDenda: boolean\\n- besaranDenda: integer",
                "id": 1,
                "type": "ClassNode"
                }
            ]
        }"""
        parser = ParseJsonToObject(data)
        result = parser.parse_classes()
        self.assertEqual(result, parser._ParseJsonToObject__classes)
        self.assertEqual(parser._ParseJsonToObject__json, json.loads(data))
        self.assertEqual(len(parser._ParseJsonToObject__json["nodes"]), 2)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["name"], "Pengelola")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["id"], 0)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["type"], "ClassNode")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["name"], "Peminjaman")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["id"], 1)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["type"], "ClassNode")
    def test_empty_nodes(self):
        data = """{
            "diagram": "ClassDiagram",
            "nodes": []
        }"""
        parser = ParseJsonToObject(data)
        result = parser.parse_classes()
        self.assertRaises(Exception)
        self.assertEqual(parser._ParseJsonToObject__json, json.loads(data))

    def test_invalid_json(self):
        data = """{
        "diagram": "ClassDiagram",
            "nodes": [
                {
                "methods": "",
                "name": "Pengelola",
                "x": 330,
                "y": 10,
                "attributes": "- isAdmin: boolean",
                "id": 0,
                "type": "ClassNode"
                },
                {
                "methods": "+ getBesaranDenda(String apalah): integer\n+ getTglPinjam(): Date\n+ getTglKembali(): Date",
                "name": "Peminjaman",
                "x": 310,
                "y": 270,
                "attributes": "- ID: String\n- isDikembalikan: boolean\n- tglPinjam: Date\n- tglKembali: Date\n- isLunasDenda: boolean\n- besaranDenda: integer",
                "id": 1,
                "type": "ClassNode"
                }
            ]"""
        
        with self.assertRaises(json.JSONDecodeError):
            parser = ParseJsonToObject(data)


    def test_missing_attributes(self):
        data = """{
            "diagram": "ClassDiagram",
            "nodes": [
                {
                "methods": "",
                "name": "Pengelola",
                "x": 330,
                "y": 10,
                "attributes": "",
                "id": 0,
                "type": "ClassNode"
                }
            ]
        }"""
        parser = ParseJsonToObject(data)
        result = parser.parse_classes()
        self.assertEqual(result, parser._ParseJsonToObject__classes)
        self.assertEqual(parser._ParseJsonToObject__json, json.loads(data))
        self.assertEqual(len(parser._ParseJsonToObject__json["nodes"]), 1)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["name"], "Pengelola")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["id"], 0)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["methods"], "")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["attributes"], "")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["type"], "ClassNode")

    def setUp(self):
        # Mocking the classes
        self.classes = {
            1: MagicMock(),
            2: MagicMock()
        }

    def test_parse_relationships_many_to_many(self):
        uml_json = {'edges':[{
                    'start': 1,
                    'end': 2,
                }]}
        multiplicities = ['10','*','1..*','1..3']
        
        for n in multiplicities:
            uml_json['edges'][0]['startLabel']=n
            for m in multiplicities:
                uml_json['edges'][0]['endLabel']=m
                self.parser = ParseJsonToObject(uml_json)
                self.parser.parse_relationships(self.classes)
                                                        
                class_from_id = self.classes[1]
                
                # Check that the ManyToManyRelationshipObject was created
                ro = class_from_id.add_relationship.call_args[0][0]
                self.assertIsInstance(ro, ManyToManyRelationshipObject)

    def test_parse_relationships_many_to_one(self):
        uml_json = {'edges':[{
                    'start': 1,
                    'end': 2,
                }]}
        multiplicities = ['10','*','1..*','1..3']
        for n in ['1']:
            uml_json['edges'][0]['startLabel']=n
            for m in multiplicities:
                uml_json['edges'][0]['endLabel']=m
                self.parser = ParseJsonToObject(uml_json)
                self.parser.parse_relationships(self.classes)
                                                        
                class_to_id = self.classes[2]
                
                ro = class_to_id.add_relationship.call_args[0][0]
                self.assertIsInstance(ro, ManyToOneRelationshipObject)
        for n in multiplicities:
            uml_json['edges'][0]['startLabel']=n
            for m in ['1']:
                uml_json['edges'][0]['endLabel']=m
                self.parser = ParseJsonToObject(uml_json)
                classes = self.parser.parse_relationships(self.classes)
                                                        
                class_from_id = self.classes[1]
                class_to_id = self.classes[2]
                
                ro = class_from_id.add_relationship.call_args[0][0]
                self.assertIsInstance(ro, ManyToOneRelationshipObject)

    def test_parse_relationships_one_to_one(self):
        uml_json = {'edges':[{
                'start': 1,
                'end': 2,
                'startLabel':'1',
                'endLabel':'1'
            }]}
        self.parser = ParseJsonToObject(uml_json)
        classes = self.parser.parse_relationships(self.classes)

        class_from_id = self.classes[1]

        ro = class_from_id.add_relationship.call_args[0][0]  # Extract the relationship object
        self.assertIsInstance(ro, OneToOneRelationshipObject)

    def test_parse_relationships_inheritance(self):
        uml_json = {'edges':[{
                'start': 1,
                'end': 2,
                'type': 'GeneralizationEdge'
            }]}
        self.parser = ParseJsonToObject(uml_json)
        classes = self.parser.parse_relationships(self.classes)
        class_from_id = self.classes[1]
        class_to_id = self.classes[2]
        
        class_from_id.set_parent.assert_called_with(class_to_id)

        # Ensure the parent is set as expected
        self.assertEqual(class_from_id.set_parent.call_args[0][0], class_to_id)

    def test_validate_amount_valid_cases(self):
        # Test valid multiplicities
        uml_json = {'edges':[{
                'start': 1,
                'end': 2,
            }]}
        self.parser = ParseJsonToObject(uml_json)
        valid_multiplicities = ['1', '*', '1..*', '0..1', '0..10']

        for amount_str in valid_multiplicities:
            uml_json['edges'][0]['endLabel']=amount_str
            try:
                self.parser._ParseJsonToObject__validate_amount(amount_str)
            except Exception as e:
                self.fail(f"__validate_amount raised an exception for a valid multiplicity: {amount_str} - {e}")
    
    def test_validate_amount_empty(self):
        with self.assertRaises(Exception):
            self.parser._ParseJsonToObject__validate_amount("")
    
    def test_validate_amount_no_max(self):
        with self.assertRaises(Exception):
            self.parser._ParseJsonToObject__validate_amount("1..")
    
    def test_validate_amount_no_min(self):
        with self.assertRaises(Exception):
            self.parser._ParseJsonToObject__validate_amount("..1")
    
    def test_validate_amount_invalid_star_placement(self):
        invalid_multiplicities = [
            "1..*1",            # Invalid range format
            "*1",               # Invalid range with "*" in the middle
        ]
        for im in invalid_multiplicities:
            with self.assertRaises(Exception):
                self.parser._ParseJsonToObject__validate_amount(im)
    
    def test_validate_amount_invalid_titik_count(self):
        invalid_multiplicities = [
            "1.1",            # Invalid range format
            "1.....*",               # Invalid range with "*" in the middle
            "1.*"               # Invalid use of "*"
        ]
        for im in invalid_multiplicities:
            with self.assertRaises(Exception):
                self.parser._ParseJsonToObject__validate_amount(im)

if __name__ == '__main__':
    unittest.main()