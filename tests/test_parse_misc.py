import unittest

from app.parse_json_to_object_seq import ParseJsonToObjectSeq


class TestParseMisc(unittest.TestCase):
    def setUp(self):
        self.parser = ParseJsonToObjectSeq()

    def test_set_return_edge_positive(self):
        with open("tests/testdata/parse_misc_positive.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()
            self.assertEqual(self.parser.get_return_edge(), "Success")

    def test_set_return_edge_negative(self):
        with open("tests/testdata/parse_misc_negative.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()
            self.assertEqual(self.parser.get_return_edge(), "Error")
