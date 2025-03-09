import unittest

from app.parse_json_to_object_seq import ParseJsonToObjectSeq


class TestParseMisc(unittest.TestCase):
    def setUp(self):
        self.parser = ParseJsonToObjectSeq()

    def test_parse_return_edge_positive(self):
        with open("tests/testdata/parse_misc_positive.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()
            print(self.parser.get_method_call())
            self.assertEqual(self.parser.parse_return_edge(), "Success")

    def test_parse_return_edge_label_invalid(self):
        with open("tests/testdata/parse_misc_negative1.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()

            with self.assertRaises(ValueError) as context:
                self.parser.parse_return_edge()
                self.assertEqual(
                    context.exception,
                    "Return edge label must be a valid variable name! Given: @return",
                )

    def test_parse_return_edge_no_call_edge(self):
        with open("tests/testdata/parse_misc_negative2.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()

            with self.assertRaises(ValueError) as context:
                self.parser.parse_return_edge()
                self.assertEqual(
                    context.exception,
                    f"Return edge must have a corresponding call edge! {6} -> {3}",
                )
