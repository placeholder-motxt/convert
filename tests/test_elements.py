import unittest
from unittest import mock

from app.models.elements import ModelsElements, ViewsElements


class TestModelsElements(unittest.TestCase):
    def test_models_elements_valid_filename(self):
        obj = ModelsElements("model_file.py")
        self.assertIsInstance(obj, ModelsElements)

    def test_models_elements_invalid_filename_type(self):
        with self.assertRaises(AssertionError):
            ModelsElements(123)  # Invalid type

    def test_models_elements_empty_filename(self):  # cornercase
        with self.assertRaises(AssertionError):
            ModelsElements("")

    def test_parse(self):
        obj = ModelsElements("string")
        with mock.patch("app.models.elements.ParseJsonToObjectClass") as MockParser:
            mock_parser_instance = MockParser.return_value
            mock_parser_instance.parse_classes.return_value = [mock.Mock()]

            self.assertEqual(
                obj.parse("content"), mock_parser_instance.parse_classes.return_value
            )

    def test_print_django_style_not_implemented(self):
        obj = ModelsElements("models.py")
        obj.parse(open("tests/test_input.txt", "r").read())
        res = obj.print_django_style()
        f = open("tests/test_result.txt", "r")
        assert res == f.read()


class TestViewsElements(unittest.TestCase):
    def setUp(self):
        self.views_elements = ViewsElements("view_file.py")

    def test_instance_of_file_elements(self):
        self.assertIsInstance(self.views_elements, ViewsElements)

    def test_print_django_style_no_methods(self):
        expected_output = ""
        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_one_controller_method(self):
        mock_controller_method = mock.Mock()
        mock_controller_method.print_django_style.return_value = (
            "def sample_controller(request):\n\tpass\n"
        )
        self.views_elements.add_controller_method(mock_controller_method)
        expected_output = "def sample_controller(request):\n\tpass\n"
        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_multiple_controller_methods(self):
        mock_controller_method1 = mock.Mock()
        mock_controller_method1.print_django_style.return_value = (
            "def controller_one(request):\n\tpass\n"
        )
        mock_controller_method2 = mock.Mock()
        mock_controller_method2.print_django_style.return_value = (
            "def controller_two(request):\n\tpass\n"
        )

        self.views_elements.add_controller_method(mock_controller_method1)
        self.views_elements.add_controller_method(mock_controller_method2)

        expected_output = (
            "def controller_one(request):\n"
            "\tpass\n"
            "def controller_two(request):\n"
            "\tpass\n"
        )

        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_class_methods(self):
        mock_class_method_1 = mock.Mock()
        mock_class_method_1.get_name.return_value = "Class1"
        mock_class_method_1.to_views_code.return_value = (
            "def class_method():\n\tmethod_call = inner_method1(arg1, arg2)"
        )
        mock_class_method_2 = mock.Mock()
        mock_class_method_2.get_name.return_value = "Class2"
        mock_class_method_2.to_views_code.return_value = (
            "def class_method():\n\tmethod_call = inner_method2(arg1, arg2)"
        )
        self.views_elements.add_class_method(mock_class_method_1)
        self.views_elements.add_class_method(mock_class_method_2)
        self.assertEqual(
            self.views_elements.print_django_style(),
            (
                "#-----method from class Class1------\n\n"
                "def class_method():\n"
                "\tmethod_call = inner_method1(arg1, arg2)\n\n\n"
                "#-----method from class Class2------\n\n"
                "def class_method():\n"
                "\tmethod_call = inner_method2(arg1, arg2)\n\n\n"
            ),
        )

    def test_print_django_style_with_one_class_method(self):
        mock_class_method_1 = mock.Mock()
        mock_class_method_1.get_name.return_value = "Class1"
        mock_class_method_1.to_views_code.return_value = (
            "def class_method():\n\tmethod_call = inner_method1(arg1, arg2)"
        )
        self.views_elements.add_class_method(mock_class_method_1)
        self.assertEqual(
            self.views_elements.print_django_style(),
            (
                "#-----method from class Class1------\n\n"
                "def class_method():\n"
                "\tmethod_call = inner_method1(arg1, arg2)\n\n\n"
            ),
        )


if __name__ == "__main__":
    unittest.main()
