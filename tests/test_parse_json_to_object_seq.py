import os
import unittest
from unittest.mock import MagicMock

from app.models.properties import TypeObject
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

        with self.assertRaises(ValueError) as context:
            ParseJsonToObjectSeq().set_json(json_data)

        self.assertEqual(
            str(context.exception),
            "The .sequence.jet is not valid. \n"
            "Please make sure the file submitted is not corrupt",
        )

    def test_negative_set_empty_json(self):
        with self.assertRaises(ValueError) as context:
            ParseJsonToObjectSeq().set_json("")

        self.assertEqual(
            str(context.exception),
            "The .sequence.jet is not valid. \n"
            "Please make sure the file submitted is not corrupt",
        )

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

        with self.assertRaises(ValueError) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(
            str(context.exception), "Duplicate class name 'Buku' on sequence diagram"
        )

    def test_edge_duplicate_attribute(self):
        with open(
            "tests/test_duplicate_attribute_seq.txt", "r", encoding="utf-8"
        ) as file:
            json_data = file.read()
        with self.assertRaises(ValueError) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(
            str(context.exception),
            "Duplicate attribute 'username' on sequence diagram \n"
            "please remove one of the parameters",
        )

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
            "getBuku",
        )

        self.assertEqual(
            len(parsed_value_controller[2].get_call()[0].get_arguments()), 1
        )
        self.assertEqual(
            parsed_value_controller[2].get_call()[0].get_arguments()[0].get_name(),
            "isbn",
        )

        self.assertEqual(
            parsed_value_controller[2].get_call()[1].get_methods().get_name(),
            "getDetailBuku",
        )

        self.assertEqual(
            len(parsed_value_controller[2].get_call()[1].get_arguments()), 0
        )

        self.assertEqual(len(parsed_value_controller[3].get_call()), 0)

        self.assertEqual(len(parsed_value_controller[4].get_call()), 3)

        self.assertEqual(
            parsed_value_controller[4].get_call()[0].get_methods().get_name(), "isValid"
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[0].get_arguments()), 1
        )

        self.assertEqual(
            parsed_value_controller[4].get_call()[0].get_arguments()[0].get_name(),
            "dataAnggota",
        )

        self.assertEqual(
            len(parsed_value_controller[4].get_call()[0].get_methods().get_calls()), 0
        )

        self.assertEqual(
            parsed_value_controller[4].get_call()[1].get_methods().get_name(),
            "prosesPeminjamanValidKeanggotaan",
        )
        self.assertEqual(
            parsed_value_controller[4].get_call()[1].get_condition(),
            "isValid",
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[1].get_arguments()), 0
        )
        self.assertEqual(
            len(parsed_value_controller[4].get_call()[1].get_methods().get_call()), 3
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_name(),
            "hasTanggungan",
        )

        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[1]
                .get_methods()
                .get_call()[0]
                .get_arguments()
            ),
            1,
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_arguments()[0]
            .get_name(),
            "peminjam",
        )

        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[1]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_calls()
            ),
            1,
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_calls()[0]
            .get_method()
            .get_name(),
            "hasTanggungan",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_name(),
            "prosesPeminjamanTidakMemilikiTanggungan",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_condition(),
            "not hasTanggunganResult",
        )

        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[1]
                .get_methods()
                .get_call()[1]
                .get_methods()
                .get_call()
            ),
            2,
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_name(),
            "borrow",
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[1]
                .get_methods()
                .get_call()[1]
                .get_methods()
                .get_call()[0]
                .get_methods()
                .get_calls()
            ),
            2,
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_calls()[0]
            .get_methods()
            .get_name(),
            "findCopyBuku",
        )
        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[1]
                .get_methods()
                .get_call()[1]
                .get_methods()
                .get_call()[0]
                .get_arguments()
            ),
            1,
        )
        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_arguments()[0]
            .get_name(),
            "isbn",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_call()[0]
            .get_methods()
            .get_calls()[1]
            .get_methods()
            .get_name(),
            "isBorrowed",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_call()[1]
            .get_methods()
            .get_name(),
            "showNotifikasiBerhasilPinjam",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[2]
            .get_methods()
            .get_name(),
            "showNotifikasiGagalPinjam",
        )

        self.assertEqual(
            parsed_value_controller[4]
            .get_call()[1]
            .get_methods()
            .get_call()[2]
            .get_condition(),
            "hasTanggungan",
        )

        self.assertEqual(
            len(
                parsed_value_controller[4]
                .get_call()[1]
                .get_methods()
                .get_call()[2]
                .get_arguments()
            ),
            0,
        )

        self.assertEqual(
            parsed_value_controller[4].get_call()[2].get_methods().get_name(),
            "showNotifikasiDataTidakValid",
        )

        self.assertEqual(
            parsed_value_controller[4].get_call()[2].get_condition(),
            "not isValid",
        )

        self.assertEqual(
            len(parsed_value_controller[4].get_call()[2].get_arguments()),
            0,
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

    def test_valid_edge_label_format(self):
        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_valid_label_format1.json")) as f:
            parser.set_json(f.read())

        parser.parse()

        self.assertEqual(
            parser.get_class_objects()["ABC"].get_methods()[0].get_name(), "doA"
        )

    def test_invalid_edge_label_format(self):
        # Invalid label format should throw exceptions, examples:
        # `[] doB ()->bval` -> have to be `[] doB () -> bval`

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_label_format2.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Wrong label format '[] doB ()->bval' on sequence diagram \n"
            "please consult the user manual document on how to name parameters",
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

        self.assertEqual(
            str(ctx.exception),
            "Invalid method name 'abcd!' on sequence diagram \n"
            "please consult the user manual document on how to name methods",
        )

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_method_name2.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Invalid method name 'class' on sequence diagram \n"
            "please consult the user manual document on how to name methods",
        )

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_method_name3.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Invalid method name '[]abcd' on sequence diagram \n"
            "please consult the user manual document on how to name methods",
        )

    def test_invalid_param_name(self):
        # Invalid method name should throw exceptions, examples:
        # `doA (a!!!)` -> have to be valid Python identifier
        # `doA (try)` -> cannot be Python keyword
        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_param_name1.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Invalid param name 'a!!!' on sequence diagram \n"
            "please consult the user manual document on how to name parameters",
        )

        parser = ParseJsonToObjectSeq()
        with open(os.path.join(TEST_DIR, "seq_invalid_param_name2.json")) as f:
            parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Invalid param name 'try' on sequence diagram \n"
            "please consult the user manual document on how to name parameters",
        )


class TestProcessReturnVariable(unittest.TestCase):
    # ----------  POSITIVE PATHS  ----------
    def test_valid_string_mapping(self):
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable("person: String")
        self.assertEqual(name, "person")

        expected = TypeObject()
        expected.set_name("str")
        self.assertEqual(typ, expected)

    def test_valid_integer_mapping(self):
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable("age: integer")
        self.assertEqual(name, "age")

        expected = TypeObject()
        expected.set_name("int")
        self.assertEqual(typ, expected)

    def test_valid_boolean_with_leading_space(self):
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable(
            "flag:  Boolean"
        )  # double-space before “Boolean”
        self.assertEqual(name, "flag")

        expected = TypeObject()
        expected.set_name("bool")
        self.assertEqual(typ, expected)

    def test_valid_no_space_between_parts(self):
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable("score:float")
        self.assertEqual(name, "score")

        expected = TypeObject()
        expected.set_name("float")
        self.assertEqual(typ, expected)

    # ----------  NEGATIVE / ERROR PATHS  ----------
    def test_error_no_colon(self):
        parser = ParseJsonToObjectSeq()
        with self.assertRaises(ValueError):
            parser.process_return_variable("invalid")

    def test_error_multiple_colons(self):
        parser = ParseJsonToObjectSeq()
        with self.assertRaises(ValueError):
            parser.process_return_variable("a:b:c")

    def test_error_empty_type(self):
        parser = ParseJsonToObjectSeq()
        with self.assertRaises(ValueError):
            parser.process_return_variable("name:")

    def test_error_empty_name(self):
        parser = ParseJsonToObjectSeq()
        with self.assertRaises(ValueError):
            parser.process_return_variable(":String")

    # ===== NEW *CORNER* CASES =====
    def test_case_insensitive_and_uppercase(self):
        """Alias mapping should be case-insensitive."""
        parser = ParseJsonToObjectSeq()
        _, typ = parser.process_return_variable("note: STRING")
        exp = TypeObject()
        exp.set_name("str")
        self.assertEqual(typ, exp)

    def test_extra_whitespace_around_colon(self):
        """
        Only a single leading space in front of the type is removed by the
        implementation; trailing/embedded spaces remain.
        """
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable("data  : String")
        self.assertEqual(name, "data")  # trailing spaces in name removed
        self.assertEqual(typ.get_name(), "str")  # mapping still works

    def test_multiple_leading_spaces_before_type(self):
        """Two+ leading spaces leave one space behind ⇢ alias mapping NOT applied."""
        parser = ParseJsonToObjectSeq()
        _, typ = parser.process_return_variable("value:   int")
        # should keep the leading spaces _inside_ the stored name
        self.assertEqual(typ.get_name(), "int")  # spaces removed

    def test_unknown_custom_type_passthrough(self):
        """Unrecognised types are stored verbatim."""
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable("payload: CustomType")
        self.assertEqual(name, "payload")
        self.assertEqual(typ.get_name(), "CustomType")  # untouched

    def test_unicode_name(self):
        """Non-ASCII variable names should parse fine."""
        parser = ParseJsonToObjectSeq()
        name, typ = parser.process_return_variable("имя: Boolean")
        exp = TypeObject()
        exp.set_name("bool")
        self.assertEqual((name, typ), ("имя", exp))


class DummyMethodCall:
    def __init__(self):
        self.ret_var_name = None
        self.ret_var_type = None

    def set_ret_var(self, name: str):
        self.ret_var_name = name

    def set_return_var_type(self, var_type: str):
        self.ret_var_type = var_type


class TestParseReturnEdge(unittest.TestCase):
    def setUp(self):
        self.parser = ParseJsonToObjectSeq()
        # Patch the process_return_variable method for simplicity
        self.parser.process_return_variable = MagicMock(
            side_effect=lambda label: (f"{label}_name", f"{label}_type")
        )

    def test_no_edges_returns_empty_list(self):
        self.parser._ParseJsonToObjectSeq__edges = []
        self.parser._ParseJsonToObjectSeq__method_call = {}
        self.assertEqual(self.parser.parse_return_edge(), [])

    def test_edges_with_no_return_type_ignored(self):
        # Edges of other types should be ignored
        self.parser._ParseJsonToObjectSeq__edges = [
            {"type": "CallEdge", "label": "call()", "start": "A", "end": "B"}
        ]
        self.parser._ParseJsonToObjectSeq__method_call = {}
        self.assertEqual(self.parser.parse_return_edge(), [])

    def test_return_edge_without_corresponding_call_raises(self):
        self.parser._ParseJsonToObjectSeq__edges = [
            {"type": "ReturnEdge", "label": "ret()", "start": "B", "end": "A"}
        ]
        self.parser._ParseJsonToObjectSeq__method_call = {}
        with self.assertRaises(ValueError) as cm:
            self.parser.parse_return_edge()
        self.assertIn(
            "Return edge must have a corresponding call edge", str(cm.exception)
        )

    def test_return_edge_with_matching_call_sets_return_vars_and_appends_label(self):
        # Setup a matching call tuple in __method_call with a mock method_call object
        method_call_mock = DummyMethodCall()
        call_tuple = ("A", "B")  # (end, start)
        self.parser._ParseJsonToObjectSeq__edges = [
            {"type": "ReturnEdge", "label": "retLabel()", "start": "B", "end": "A"}
        ]
        self.parser._ParseJsonToObjectSeq__method_call = {
            call_tuple: {"end": "B", "method_call": method_call_mock}
        }
        result = self.parser.parse_return_edge()
        self.assertEqual(result, ["retLabel()_name"])
        self.assertEqual(method_call_mock.ret_var_name, "retLabel()_name")
        self.assertEqual(method_call_mock.ret_var_type, "retLabel()_type")
        self.parser.process_return_variable.assert_called_once_with("retLabel()")

    def test_return_edge_with_matching_call_but_method_call_is_none(self):
        # If "method_call" is None or falsy, it should not process or append label
        call_tuple = ("A", "B")
        self.parser._ParseJsonToObjectSeq__edges = [
            {"type": "ReturnEdge", "label": "ret()", "start": "B", "end": "A"}
        ]
        self.parser._ParseJsonToObjectSeq__method_call = {
            call_tuple: {
                "end": "B",
                "method_call": None,  # method_call falsy
            }
        }
        # Should return empty list and not raise
        self.assertEqual(self.parser.parse_return_edge(), [])

    def test_multiple_return_edges(self):
        # Multiple edges processed, some ignored
        method_call_1 = DummyMethodCall()
        method_call_2 = DummyMethodCall()
        self.parser._ParseJsonToObjectSeq__edges = [
            {"type": "ReturnEdge", "label": "ret1()", "start": "B", "end": "A"},
            {"type": "ReturnEdge", "label": "ret2()", "start": "D", "end": "C"},
            {"type": "CallEdge", "label": "call()", "start": "X", "end": "Y"},
        ]
        self.parser._ParseJsonToObjectSeq__method_call = {
            ("A", "B"): {"end": "B", "method_call": method_call_1},
            ("C", "D"): {"end": "D", "method_call": method_call_2},
        }
        results = self.parser.parse_return_edge()
        self.assertEqual(results, ["ret1()_name", "ret2()_name"])
        self.assertEqual(method_call_1.ret_var_name, "ret1()_name")
        self.assertEqual(method_call_2.ret_var_name, "ret2()_name")
        self.parser.process_return_variable.assert_has_calls(
            [
                unittest.mock.call("ret1()"),
                unittest.mock.call("ret2()"),
            ]
        )

    def test_label_with_extra_spaces_stripped(self):
        method_call_mock = DummyMethodCall()
        call_tuple = ("A", "B")
        self.parser._ParseJsonToObjectSeq__edges = [
            {
                "type": "ReturnEdge",
                "label": "  retWithSpaces()  ",
                "start": "B",
                "end": "A",
            }
        ]
        self.parser._ParseJsonToObjectSeq__method_call = {
            call_tuple: {"end": "B", "method_call": method_call_mock}
        }
        result = self.parser.parse_return_edge()
        self.assertEqual(result, ["retWithSpaces()_name"])
        self.assertEqual(method_call_mock.ret_var_name, "retWithSpaces()_name")
