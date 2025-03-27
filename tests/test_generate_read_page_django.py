import unittest
from unittest.mock import MagicMock, patch

import pytest

from app.generate_frontend.read.generate_read_page_django import (
    generate_html_read_page_django,
    generate_html_read_pages_django,
)
from app.models.diagram import ClassObject, FieldObject
from app.models.elements import ModelsElements


# Tests for generate_html_read_page_django
class TestGenerateHTMLReadPageDjango(unittest.TestCase):
    @patch("app.generate_frontend.read.generate_read_page_django.render_template")
    def test_generate_html_read_page_django_positive(
        self, mock_render_template: MagicMock
    ):
        """Positive case: Valid class with fields renders correct context."""
        # Create a ClassObject with a name and two fields
        class_obj = ClassObject()
        class_obj.set_name("Person")
        field1 = FieldObject()
        field1.set_name("name")
        field2 = FieldObject()
        field2.set_name("age")
        class_obj.add_field(field1)
        class_obj.add_field(field2)

        # Expected context (assuming camel_to_snake converts "Person" to "person")
        expected_context = {
            "class_name": "Person",
            "class_snake": "person",
            "fields": [{"name": "name"}, {"name": "age"}],
        }

        # Set up the mock to return a dummy rendered string.
        mock_render_template.return_value = "Rendered Person Page"
        result = generate_html_read_page_django(class_obj)

        # Verify that render_template was called with the expected arguments.
        mock_render_template.assert_called_once_with(
            "read_page_django.html.j2", expected_context
        )
        self.assertEqual(result, "Rendered Person Page")

    def test_generate_html_read_pages_django_negative_type_error(self):
        with pytest.raises(TypeError):
            generate_html_read_pages_django("test")

    @patch("app.generate_frontend.read.generate_read_page_django.render_template")
    def test_generate_html_read_page_django_negative_template_failure(
        self, mock_render_template: MagicMock
    ):
        """Negative case: Simulate a template rendering failure by returning an empty string."""
        class_obj = ClassObject()
        class_obj.set_name("Person")
        # No fields added

        # Simulate failure in rendering (empty result)
        mock_render_template.return_value = ""
        result = generate_html_read_page_django(class_obj)
        self.assertEqual(result, "")

    @patch("app.generate_frontend.read.generate_read_page_django.render_template")
    def test_generate_html_read_page_django_corner_empty_fields(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Class with no fields should yield an empty fields list in context."""
        class_obj = ClassObject()
        class_obj.set_name("EmptyClass")
        # Do not add any fields
        expected_context = {
            "class_name": "EmptyClass",
            "class_snake": "empty_class",
            "fields": [],
        }
        mock_render_template.return_value = "Rendered EmptyClass Page"
        result = generate_html_read_page_django(class_obj)
        mock_render_template.assert_called_once_with(
            "read_page_django.html.j2", expected_context
        )
        self.assertEqual(result, "Rendered EmptyClass Page")

    @patch("app.generate_frontend.read.generate_read_page_django.render_template")
    def test_generate_html_read_page_django_corner_empty_class_name(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Class with an empty name should produce empty string for both class_name
        and class_snake."""
        class_obj = ClassObject()
        class_obj.set_name("")
        expected_context = {
            "class_name": "",
            "class_snake": "",
            "fields": [],
        }
        mock_render_template.return_value = "Rendered Empty Name Page"
        result = generate_html_read_page_django(class_obj)
        mock_render_template.assert_called_once_with(
            "read_page_django.html.j2", expected_context
        )
        self.assertEqual(result, "Rendered Empty Name Page")

    @patch("app.generate_frontend.read.generate_read_page_django.render_template")
    def test_generate_html_read_page_django_corner_field_empty_name(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Class with a field that has an empty name."""
        class_obj = ClassObject()
        class_obj.set_name("Person")
        field = FieldObject()
        field.set_name("")
        class_obj.add_field(field)

        expected_context = {
            "class_name": "Person",
            "class_snake": "person",
            "fields": [{"name": ""}],
        }
        mock_render_template.return_value = "Rendered with empty field name"
        result = generate_html_read_page_django(class_obj)
        mock_render_template.assert_called_once_with(
            "read_page_django.html.j2", expected_context
        )
        self.assertEqual(result, "Rendered with empty field name")

    @patch("app.generate_frontend.read.generate_read_page_django.render_template")
    def test_generate_html_read_page_django_corner_special_characters(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Class name and field names with special characters."""
        class_obj = ClassObject()
        class_obj.set_name("Test-Class")
        field = FieldObject()
        field.set_name("field name")
        class_obj.add_field(field)

        # Assuming camel_to_snake simply lowercases without handling hyphens or spaces specially.
        expected_context = {
            "class_name": "Test-Class",
            "class_snake": "test-class",
            "fields": [{"name": "field name"}],
        }
        mock_render_template.return_value = "Rendered Special Characters Page"
        result = generate_html_read_page_django(class_obj)
        mock_render_template.assert_called_once_with(
            "read_page_django.html.j2", expected_context
        )
        self.assertEqual(result, "Rendered Special Characters Page")


# Tests for generate_html_read_pages_django
class TestGenerateHTMLReadPagesDjango(unittest.TestCase):
    @patch(
        "app.generate_frontend.read.generate_read_page_django.generate_html_read_page_django"
    )
    def test_generate_html_read_pages_django_positive(
        self, mock_generate_page: MagicMock
    ):
        """Positive case: Multiple classes are processed into a list of rendered pages."""
        models_elements = ModelsElements("test_file")
        class_obj1 = ClassObject()
        class_obj1.set_name("Person")
        class_obj1.set_is_public(True)
        class_obj2 = ClassObject()
        class_obj2.set_name("Vehicle")
        class_obj2.set_is_public(True)
        models_elements.add_class(class_obj1)
        models_elements.add_class(class_obj2)

        # Setup the side effect so each call returns a distinct string.
        mock_generate_page.side_effect = [
            "Rendered Person Page",
            "Rendered Vehicle Page",
        ]

        result = generate_html_read_pages_django(models_elements)
        self.assertEqual(result, ["Rendered Person Page", "Rendered Vehicle Page"])
        self.assertEqual(mock_generate_page.call_count, 2)

    def test_generate_html_read_page_django_negative_type_error(self):
        with pytest.raises(TypeError):
            generate_html_read_page_django("test")

    def test_generate_html_read_pages_django_negative_no_classes(self):
        """Negative case: When no classes exist, an empty list should be returned."""
        models_elements = ModelsElements("test_file")
        result = generate_html_read_pages_django(models_elements)
        self.assertEqual(result, [])

    @patch(
        "app.generate_frontend.read.generate_read_page_django.generate_html_read_page_django"
    )
    def test_generate_html_read_pages_django_corner_mixed_cases(
        self, mock_generate_page: MagicMock
    ):
        """Corner case: Mix of classes, one with fields and one without."""
        models_elements = ModelsElements("test_file")
        class_obj1 = ClassObject()
        class_obj1.set_name("Person")
        class_obj1.set_is_public(True)
        field = FieldObject()
        field.set_name("name")
        class_obj1.add_field(field)

        class_obj2 = ClassObject()
        class_obj2.set_name("EmptyClass")
        class_obj2.set_is_public(True)
        models_elements.add_class(class_obj1)
        models_elements.add_class(class_obj2)

        mock_generate_page.side_effect = [
            "Rendered Person Page",
            "Rendered EmptyClass Page",
        ]
        result = generate_html_read_pages_django(models_elements)
        self.assertEqual(result, ["Rendered Person Page", "Rendered EmptyClass Page"])
        self.assertEqual(mock_generate_page.call_count, 2)

    @patch(
        "app.generate_frontend.read.generate_read_page_django.generate_html_read_page_django"
    )
    def test_generate_html_read_pages_django_corner_duplicate_class_names(
        self, mock_generate_page: MagicMock
    ):
        """Corner case: Duplicate class names in ModelsElements should be processed separately."""
        models_elements = ModelsElements("test_file")
        class_obj1 = ClassObject()
        class_obj1.set_name("Person")
        class_obj1.set_is_public(True)
        class_obj2 = ClassObject()
        class_obj2.set_name("Person")  # duplicate name
        class_obj2.set_is_public(True)
        models_elements.add_class(class_obj1)
        models_elements.add_class(class_obj2)
        mock_generate_page.side_effect = [
            "Rendered Person Page 1",
            "Rendered Person Page 2",
        ]
        result = generate_html_read_pages_django(models_elements)
        self.assertEqual(result, ["Rendered Person Page 1", "Rendered Person Page 2"])
        self.assertEqual(mock_generate_page.call_count, 2)

    @patch(
        "app.generate_frontend.read.generate_read_page_django.generate_html_read_page_django"
    )
    def test_generate_html_read_pages_django_corner_large_number(
        self, mock_generate_page: MagicMock
    ):
        """Corner case: Handle a large number of classes."""
        models_elements = ModelsElements("test_file")
        num_classes = 100
        rendered_pages = []
        for i in range(num_classes):
            class_obj = ClassObject()
            class_obj.set_name(f"Class{i}")
            class_obj.set_is_public(True)
            models_elements.add_class(class_obj)
            rendered_pages.append(f"Rendered Class{i} Page")
        mock_generate_page.side_effect = rendered_pages
        result = generate_html_read_pages_django(models_elements)
        self.assertEqual(result, rendered_pages)
        self.assertEqual(mock_generate_page.call_count, num_classes)
