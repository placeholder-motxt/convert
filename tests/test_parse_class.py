import unittest
from app.parse_json_to_object import ParseJsonToObject
from app.element_objects import *
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
                "methods": "+ getBesaranDenda(String apalah): integer\n+ getTglPinjam(): Date\n+ getTglKembali(): Date",
                "name": "Peminjaman",
                "x": 310,
                "y": 270,
                "attributes": "- ID: String\n- isDikembalikan: boolean\n- tglPinjam: Date\n- tglKembali: Date\n- isLunasDenda: boolean\n- besaranDenda: integer",
                "id": 1,
                "type": "ClassNode"
                },
            ]
        }"""
        parser = ParseJsonToObject(data)
        result = parser.parse()
        self.assertEqual(result, "Done")
        self.assertEqual(parser._ParseJsonToObject__json, data)
        self.assertEqual(len(parser._ParseJsonToObject__json["nodes"]), 2)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["name"], "Pengelola")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["id"], 0)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["methods"], "")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["attributes"], "- isAdmin: boolean")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["type"], "ClassNode")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["name"], "Peminjaman")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["id"], 1)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["methods"], "+ getBesaranDenda(String apalah): integer\n+ getTglPinjam(): Date\n+ getTglKembali(): Date")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["attributes"], "- ID: String\n- isDikembalikan: boolean\n- tglPinjam: Date\n- tglKembali: Date\n- isLunasDenda: boolean\n- besaranDenda: integer")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][1]["type"], "ClassNode")

    def test_empty_nodes(self):
        data = """{
            "diagram": "ClassDiagram",
            "nodes": []
        }"""
        parser = ParseJsonToObject(data)
        result = parser.parse()
        self.assertEqual(result, "Error: value key is missing")
        self.assertEqual(parser._ParseJsonToObject__json, data)
        self.assertEqual(len(parser._ParseJsonToObject__json["nodes"]), 0)

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
            ]
        """
        parser = ParseJsonToObject(data)
        result = parser.parse()
        self.assertEqual(result, "Error: json is not valid")
        self.assertEqual(parser._ParseJsonToObject__json, data)


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
        result = parser.parse()
        self.assertEqual(result, "Done")
        self.assertEqual(parser._ParseJsonToObject__json, data)
        self.assertEqual(len(parser._ParseJsonToObject__json["nodes"]), 1)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["name"], "Pengelola")
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["id"], 0)
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["methods"], "")
        self.assertNotIn("attributes", parser._ParseJsonToObject__json["nodes"][0])
        self.assertEqual(parser._ParseJsonToObject__json["nodes"][0]["type"], "ClassNode")

if __name__ == '__main__':
    unittest.main()