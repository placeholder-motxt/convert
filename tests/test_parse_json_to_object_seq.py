import os
import unittest

from app.parse_json_to_object_seq import ParseJsonToObjectSeq

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


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
        with open(
            "tests/test_duplicate_class_name_seq.txt", "r", encoding="utf-8"
        ) as file:
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
        with open(
            "tests/test_duplicate_attribute_seq.txt", "r", encoding="utf-8"
        ) as file:
            json_data = file.read()
        with self.assertRaises(Exception) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(str(context.exception), "Duplicate attribute!")

    def test_positive_class_object(self):
        with open("tests/test_valid_json_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        parser = ParseJsonToObjectSeq()
        parser.set_json(json_data)
        parser.parse()

        parsed_value = parser.get_class_objects()
        self.assertEqual(
            parsed_value["Buku"].get_methods()[0].get_name(), "getDetailBuku"
        )

        self.assertEqual(
            parsed_value["ListBuku"].get_methods()[0].get_name(), "getBuku"
        )
        self.assertEqual(
            parsed_value["ListBuku"].get_methods()[0].get_parameters()[0].get_name(),
            "isbn",
        )

        self.assertEqual(
            parsed_value["ListPeminjam"].get_methods()[0].get_name(), "isValid"
        )
        self.assertEqual(
            parsed_value["ListPeminjam"]
            .get_methods()[0]
            .get_parameters()[0]
            .get_name(),
            "dataAnggota",
        )
        self.assertEqual(
            parsed_value["ListPeminjam"].get_methods()[1].get_name(), "hasTanggungan"
        )
        self.assertEqual(
            parsed_value["ListPeminjam"]
            .get_methods()[1]
            .get_parameters()[0]
            .get_name(),
            "peminjam",
        )

        self.assertEqual(
            parsed_value["Peminjam"].get_methods()[0].get_name(), "hasTanggungan"
        )

        self.assertEqual(parsed_value["ListCopy"].get_methods()[0].get_name(), "borrow")
        self.assertEqual(
            parsed_value["ListCopy"].get_methods()[0].get_parameters()[0].get_name(),
            "isbn",
        )

        self.assertEqual(
            parsed_value["CopyBuku"].get_methods()[0].get_name(), "isBorrowed"
        )

    def test_positive_method_call_object(self):
        with open("tests/test_valid_json_seq.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        parser = ParseJsonToObjectSeq()
        parser.set_json(json_data)
        parser.parse()

        parsed_value_class_object = parser.get_class_objects()
        parsed_value_controller = parser.get_controller_method()

        self.assertEqual(len(parsed_value_controller[0].get_call()), 0)

        self.assertEqual(len(parsed_value_controller[1].get_call()), 0)

        self.assertEqual(len(parsed_value_controller[2].get_call()), 2)
        self.assertEqual(
            parsed_value_controller[2].get_call()[0].get_methods().get_name(),
            "getDetailBuku",
        )
        self.assertEqual(
            len(parsed_value_controller[2].get_call()[0].get_arguments()), 0
        )
        self.assertEqual(
            parsed_value_controller[2].get_call()[1].get_methods().get_name(), "getBuku"
        )
        self.assertEqual(
            len(parsed_value_controller[2].get_call()[1].get_arguments()), 1
        )
        self.assertEqual(
            parsed_value_controller[2].get_call()[1].get_arguments()[0].get_name(),
            "isbn",
        )

        self.assertEqual(len(parsed_value_controller[3].get_call()), 0)

        self.assertEqual(len(parsed_value_controller[4].get_call()), 3)
        self.assertEqual(
            parsed_value_controller[4].get_call()[0].get_methods().get_name(),
            "prosesPeminjamanValidKeanggotaan",
        )
        self.assertEqual(
            parsed_value_controller[4].get_call()[0].get_condition(),
            "isValid",
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[0].get_arguments()), 0
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[0].get_methods().get_call()), 3
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_name(),
            "prosesPeminjamanTidakMemilikiTanggungan",
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_call()
            ),
            2,
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_name(),
            "showNotifikasiBerhasilPinjam",
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_call()
            ),
            0,
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_arguments()
            ),
            0,
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_name(),
            "borrow",
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_call()[1]
                .get_methods()
                .get_calls()
            ),
            2,
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_calls()[0]
            .get_methods()
            .get_name(),
            "isBorrowed",
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_calls()[1]
            .get_methods()
            .get_name(),
            "findCopyBuku",
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[0]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_call()[1]
                .get_arguments()
            ),
            1,
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_call()[1]
            .get_arguments()[0]
            .get_name(),
            "isbn",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_name(),
            "showNotifikasiGagalPinjam",
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[2]
            .get_methods()
            .get_name(),
            "hasTanggungan",
        )

        self.assertEqual(
            parsed_value_controller[4].get_call()[1].get_methods().get_name(),
            "showNotifikasiDataTidakValid",
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[1].get_arguments()), 0
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[1].get_methods().get_call()), 0
        )

        self.assertEqual(
            parsed_value_controller[4].get_call()[2].get_methods().get_name(), "isValid"
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[2].get_arguments()), 1
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[2].get_methods().get_calls()), 0
        )
        self.assertEqual(
            parsed_value_controller[4].get_call()[2].get_arguments()[0].get_name(),
            "dataAnggota",
        )

        self.assertEqual(
            len(parsed_value_controller[4].get_call()[0].get_methods().get_call()), 3
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_name(),
            "prosesPeminjamanTidakMemilikiTanggungan",
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_name(),
            "showNotifikasiGagalPinjam",
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[0]
            .get_methods()
            .get_call()[2]
            .get_methods()
            .get_name(),
            "hasTanggungan",
        )

        self.assertEqual(
            len(parsed_value_class_object["ListBuku"].get_methods()[0].get_calls()), 0
        )
        self.assertEqual(
            len(parsed_value_class_object["Buku"].get_methods()[0].get_calls()), 0
        )

        self.assertEqual(
            len(parsed_value_class_object["ListPeminjam"].get_methods()[0].get_calls()),
            0,
        )

    def test_invalid_edge_label_format(self):
        # Invalid label format should throw exceptions, examples:
        # `doA()` -> have to be `doA ()`
        # `[] doB ()->bval` -> have to be `[] doB () -> bval`
        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_label_format1.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Wrong label format: doA()\n"
            "Check that the format is in compliance with the guide",
        )

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_label_format2.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Wrong label format: [] doB ()->bval\n"
            "Check that the format is in compliance with the guide",
        )

    def test_invalid_method_name(self):
        # Invalid method name should throw exceptions, examples:
        # `abcd! ()` -> have to be valid Python identifier
        # `class ()` -> cannot be Python keyword
        # `[]abcd ()` -> `[]` is counted as part of the method name
        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_method_name1.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(str(ctx.exception), "Invalid method name: abcd!")

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_method_name2.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(str(ctx.exception), "Invalid method name: class")

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_method_name3.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(str(ctx.exception), "Invalid method name: []abcd")

    def test_invalid_param_name(self):
        # Invalid method name should throw exceptions, examples:
        # `doA (a!!!)` -> have to be valid Python identifier
        # `doA (try)` -> cannot be Python keyword
        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_param_name1.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(str(ctx.exception), "Invalid param name: a!!!")

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_param_name2.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(str(ctx.exception), "Invalid param name: try")
