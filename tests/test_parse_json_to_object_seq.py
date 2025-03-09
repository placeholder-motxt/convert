import unittest

from app.parse_json_to_object_seq import ParseJsonToObjectSeq


class TestParseJsonToObjectSeq(unittest.TestCase):
    def test_set_valid_json(self):
        with open("tests/test_valid_json_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()
        self.assertEqual("Success", ParseJsonToObjectSeq().set_json(json_data))

    def test_negative_set_invalid_json(self):
        with open("tests/test_invalid_json_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with self.assertRaises(Exception) as context:
            ParseJsonToObjectSeq().set_json(json_data)

        self.assertEqual(str(context.exception), "Given .jet is not valid!")

    def test_negative_set_empty_json(self):
        with self.assertRaises(Exception) as context:
            ParseJsonToObjectSeq().set_json("")

        self.assertEqual(str(context.exception), "Given .jet is not valid!")

    def test_positive_parse_views(self):
        with open("tests/test_valid_json_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        parser = ParseJsonToObjectSeq()
        parser.set_json(json_data)
        parser.parse()

        parsed_value = parser.get_controller_method()

        self.assertEqual(len(parsed_value), 10)

        self.assertEqual(parsed_value[0].get_name(), "login")
        self.assertEqual(len(parsed_value[0].get_parameters()), 2)
        self.assertEqual(parsed_value[0].get_parameters()[0].get_name(), "username")
        self.assertEqual(parsed_value[0].get_parameters()[1].get_name(), "password")

        self.assertEqual(parsed_value[1].get_name(), "HalamanPemrosesanPeminjaman")
        self.assertEqual(len(parsed_value[1].get_parameters()), 0)

        self.assertEqual(parsed_value[2].get_name(), "LihatDetailBuku")
        self.assertEqual(len(parsed_value[2].get_parameters()), 1)
        self.assertEqual(parsed_value[2].get_parameters()[0].get_name(), "isbn")

        self.assertEqual(parsed_value[3].get_name(), "FormProsesPeminjaman")
        self.assertEqual(len(parsed_value[3].get_parameters()), 1)
        self.assertEqual(parsed_value[3].get_parameters()[0].get_name(), "isbn")

        self.assertEqual(parsed_value[4].get_name(), "SubmitProsesPeminjaman")
        self.assertEqual(len(parsed_value[4].get_parameters()), 1)
        self.assertEqual(parsed_value[4].get_parameters()[0].get_name(), "isbn")

        self.assertEqual(parsed_value[5].get_name(), "prosesPeminjamanValidKeanggotaan")
        self.assertEqual(len(parsed_value[5].get_parameters()), 0)

        self.assertEqual(
            parsed_value[6].get_name(), "prosesPeminjamanTidakMemilikiTanggungan"
        )
        self.assertEqual(len(parsed_value[6].get_parameters()), 0)

        self.assertEqual(parsed_value[7].get_name(), "showNotifikasiBerhasilPinjam")
        self.assertEqual(len(parsed_value[7].get_parameters()), 0)

        self.assertEqual(parsed_value[8].get_name(), "showNotifikasiGagalPinjam")
        self.assertEqual(len(parsed_value[8].get_parameters()), 0)

        self.assertEqual(parsed_value[9].get_name(), "showNotifikasiDataTidakValid")
        self.assertEqual(len(parsed_value[9].get_parameters()), 0)

    def test_edge_duplicate_class_name(self):
        with open("tests/test_duplicate_class_name_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with self.assertRaises(Exception) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(str(context.exception), "Duplicate class name!")

    # def test_edge_duplicate_method_name(self):
    #     with open("tests/test_duplicate_method_name_seq.txt", "r", encoding="utf-8") as file:
    #         json_data = file.read()

    #     with self.assertRaises(Exception) as context:
    #         parser = ParseJsonToObjectSeq()
    #         parser.set_json(json_data)
    #         parser.parse()
    #     self.assertEqual(str(context.exception), "Duplicate method!")

    def test_edge_duplicate_attribute(self):
        with open("tests/test_duplicate_attribute_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()
        with self.assertRaises(Exception) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(str(context.exception), "Duplicate attribute!")
