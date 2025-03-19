import os
import unittest
from pathlib import Path
from unittest import mock

import pytest

from app.models.elements import (
    ModelsElements,
    UrlsElement,
    ViewsElements,
)


class TestModelsElements(unittest.TestCase):
    def test_models_elements_valid_filename(self):
        obj = ModelsElements("model_file.py")
        self.assertIsInstance(obj, ModelsElements)

    def test_models_elements_invalid_filename_type(self):
        with self.assertRaises(TypeError):
            ModelsElements(123)  # Invalid type

    def test_models_elements_empty_filename(self):  # cornercase
        with self.assertRaises(ValueError):
            ModelsElements("")

    def test_parse(self):
        obj = ModelsElements("string")
        with mock.patch("app.models.elements.ParseJsonToObjectClass") as mock_parser:
            mock_parser_instance = mock_parser.return_value
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


class TestUrlsElements:
    def test_print_django_style(self):
        self.requirements_elements = UrlsElement("urls.py")
        mock_class = mock.Mock()
        mock_class.get_name.return_value = "Class1"
        res = self.requirements_elements.print_django_style(classes=[mock_class])
        assert (
            res == "from django.urls import path\n"
            "from .views import (\n    "
            "create_Class1,\n    "
            "get_Class1,\n    )\n\n"
            'app_name = "main"\n\n'
            "urlpatterns = [\n    "
            "path('create-class1/', create_class1, name=\"create_class1\"),\n    "
            "path('get-all-class1/', get_class1, name=\"get_class1\"),\n"
            "]"
        )

    @pytest.mark.asyncio
    async def test_write_to_file(self):
        self.requirements_elements = UrlsElement("urls.py")
        mock_class = mock.Mock()
        mock_class.get_name.return_value = "Class1"
        await self.requirements_elements.write_file(classes=[mock_class], path="./app")
        print(Path("./app/urls.py").is_file())
        assert Path("./app/urls.py").is_file()
        if Path("./app/urls.py").is_file():
            os.remove("./app/urls.py")


if __name__ == "__main__":
    unittest.main()
