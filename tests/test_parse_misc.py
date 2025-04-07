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
            result = self.parser.parse_return_edge()

            self.assertEqual(result[0], "buku")
            self.assertEqual(result[1], "detailBuku")
            self.assertEqual(result[2], "isValid")
            self.assertEqual(result[3], "hasTanggunganResult")
            self.assertEqual(result[4], "hasTanggunganResult")

    def test_parse_return_edge_label_invalid(self):
        with open("tests/testdata/parse_misc_negative1.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()

            with self.assertRaises(ValueError) as context:
                self.parser.parse_return_edge()
            self.assertEqual(
                str(context.exception),
                "Return edge label must be a valid variable name! Given '@return' \n"
                "on sequence diagram please consult the "
                "user manual document on how to name methods",
            )

    def test_parse_return_edge_no_call_edge(self):
        with open("tests/testdata/parse_misc_negative2.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()

            with self.assertRaises(ValueError) as context:
                self.parser.parse_return_edge()
            self.assertEqual(
                str(context.exception),
                "Return edge must have a corresponding call edge on sequence diagram\n"
                "6 -> 3",
            )

    def test_method_call_object_condition_positive(self):
        with open("tests/testdata/parse_misc_condition_positive.json") as file:
            json_data = file.read().replace("\n", "")
            self.parser.set_json(json_data)
            self.parser.parse()
            result = self.parser.get_method_call()
            for edge in self.parser.get_edges():
                start = edge["start"]
                end = edge["end"]
                key = (start, end)
                if result[key]["condition"] is not None and key == (25, 14):
                    self.assertEqual(result[key]["condition"], "POST")
