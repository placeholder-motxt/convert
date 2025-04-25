import unittest
from unittest import mock

from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.models.properties import FieldObject, TypeObject


class TestModelsElementsSpringBootStyle(unittest.TestCase):
    def setUp(self):
        self.models = ModelsElements("models.py")

    def test_print_springboot_style_positive_case(self):
        """Test: Positive case where valid ClassObjects are converted to Spring Boot style."""
        class_obj_1 = ClassObject()
        class_obj_1.set_name("Class1")
        class_obj_1.to_models_springboot_context = mock.Mock(
            return_value={"name": "Class1", "fields": []}
        )

        class_obj_2 = ClassObject()
        class_obj_2.set_name("Class2")
        class_obj_2.to_models_springboot_context = mock.Mock(
            return_value={"name": "Class2", "fields": []}
        )

        self.models.add_class(class_obj_1)
        self.models.add_class(class_obj_2)

        with mock.patch("app.models.elements.render_template") as mock_render_template:
            mock_render_template.side_effect = lambda template, context: (
                f"Rendered {context['name']}"
            )

            result = self.models.print_springboot_style("test_project", "com.example")

            self.assertEqual(len(result), 2)
            self.assertIn("Class1", result)
            self.assertIn("Class2", result)
            self.assertEqual(result["Class1"], "Rendered Class1")
            self.assertEqual(result["Class2"], "Rendered Class2")

    def test_print_springboot_style_negative_case_render_error(self):
        """Test: Negative case where rendering the template raises an exception."""
        class_obj = ClassObject()
        class_obj.set_name("Class1")
        class_obj.to_models_springboot_context = mock.Mock(
            return_value={"name": "Class1", "fields": []}
        )

        self.models.add_class(class_obj)

        with mock.patch(
            "app.models.elements.render_template",
            side_effect=Exception("Render error"),
        ):
            result = self.models.print_springboot_style("test_project", "com.example")

            self.assertEqual(result, {})

    def test_print_springboot_style_edge_case_no_classes(self):
        """Test: Edge case where no classes are added to the ModelsElements."""
        result = self.models.print_springboot_style("test_project", "com.example")
        self.assertEqual(result, {})

    def test_print_springboot_style_edge_case_empty_project_name(self):
        """Test: Edge case where the project name is an empty string."""
        class_obj = ClassObject()
        class_obj.set_name("Class1")
        class_obj.to_models_springboot_context = mock.Mock(
            return_value={"name": "Class1", "fields": []}
        )

        self.models.add_class(class_obj)

        with mock.patch("app.models.elements.render_template") as mock_render_template:
            mock_render_template.side_effect = lambda template, context: (
                f"Rendered {context['name']}"
            )

            result = self.models.print_springboot_style("", "com.example")

            self.assertEqual(len(result), 1)
            self.assertIn("Class1", result)
            self.assertEqual(result["Class1"], "Rendered Class1")


class TestFieldObjectSpringBootTemplate(unittest.TestCase):
    def setUp(self):
        self.field_object = FieldObject()

    def test_to_springboot_models_template_positive(self):
        self.field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("integer")
        self.field_object.set_type(type_obj)
        expected_output = {"name": "test_field", "type": "Integer"}
        self.assertEqual(
            self.field_object.to_springboot_models_template(), expected_output
        )

    def test_to_springboot_models_template_default_fallback(self):
        self.field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("unknown_type")
        self.field_object.set_type(type_obj)
        expected_output = {"name": "test_field", "type": "String"}
        self.assertEqual(
            self.field_object.to_springboot_models_template(), expected_output
        )

    def test_to_springboot_models_template_edge_case_empty_name(self):
        self.field_object.set_name("")
        type_obj = TypeObject()
        type_obj.set_name("boolean")
        self.field_object.set_type(type_obj)
        expected_output = {"name": "", "type": "boolean"}
        self.assertEqual(
            self.field_object.to_springboot_models_template(), expected_output
        )

    def test_to_springboot_models_template_edge_case_empty_type(self):
        self.field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("")
        self.field_object.set_type(type_obj)
        expected_output = {"name": "test_field", "type": "String"}
        self.assertEqual(
            self.field_object.to_springboot_models_template(), expected_output
        )

    def test_to_springboot_models_template_negative_no_name_set(self):
        type_obj = TypeObject()
        type_obj.set_name("float")
        self.field_object.set_type(type_obj)
        expected_output = {"name": "", "type": "float"}
        self.assertEqual(
            self.field_object.to_springboot_models_template(), expected_output
        )
