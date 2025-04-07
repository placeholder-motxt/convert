import unittest
from unittest.mock import MagicMock, patch

from app.generate_frontend.edit.generate_edit_page_django import (
    generate_html_edit_page_django,
    generate_html_edit_pages_django,
)
from app.models.diagram import ClassObject, FieldObject
from app.models.elements import ModelsElements


class TestGenerateHtmlEditPageDjango(unittest.TestCase):
    def setUp(self):
        self.models_elements = ModelsElements("TestModel")

        self.class_object1 = ClassObject()
        self.class_object1.set_name("Item")
        field1 = FieldObject()
        field1.set_name("name")
        field2 = FieldObject()
        field2.set_name("description")
        field3 = FieldObject()
        field3.set_name("price")
        self.class_object1.add_field(field1)
        self.class_object1.add_field(field2)
        self.class_object1.add_field(field3)

        self.class_object2 = ClassObject()
        self.class_object2.set_name("Product")
        field21 = FieldObject()
        field21.set_name("name")
        field22 = FieldObject()
        field22.set_name("model")
        self.class_object2.add_field(field21)
        self.class_object2.add_field(field22)

        self.models_elements.add_class(self.class_object1)
        self.models_elements.add_class(self.class_object2)

    def test_generate_html_edit_page_django_normal(self):
        # Normal (positive) case for HTML edit page generation
        result = generate_html_edit_page_django(self.class_object1)
        self.assertIn("<title>Edit Item</title>", result)
        self.assertIn("<h1>Edit Item</h1>", result)
        self.assertIn('<button type="submit">Save</button>', result)

    @patch("app.generate_frontend.edit.generate_edit_page_django.render_template")
    def test_generate_html_edit_page_correct_template_used(
        self, mock_render: MagicMock
    ):
        # Positive case for HTML edit page generation should use the correct template
        generate_html_edit_page_django(self.class_object2)
        ctx = {"class_name": self.class_object2.get_name()}
        mock_render.assert_called_once_with("edit_page_django.html.j2", ctx)

    def test_generate_html_create_page_django_empty_class(self):
        # Edge case where the class is somehow empty
        # (edge because it shouldn't be possible, but maybe something could go wrong)
        # should return empty string (or maybe error? open for suggestions)
        # empty means no name nor fields
        empty_class_object = ClassObject()
        result = generate_html_edit_page_django(empty_class_object)
        self.assertNotIn("<title>Edit </title>", result)
        self.assertNotIn("<h1>Edit </h1>", result)
        self.assertNotIn('<button type="submit">Save</button>', result)
        self.assertEqual(result, "")

    def test_generate_html_create_pages_django_normal(self):
        # Positive case for generating HTML pages for models elements
        result = generate_html_edit_pages_django(self.models_elements)
        self.assertEqual(len(result), 2)
        self.assertIn("<title>Edit Item</title>", result[0])
        self.assertIn("<h1>Edit Item</h1>", result[0])
        self.assertIn('<button type="submit">Save</button>', result[0])
        self.assertIn("<title>Edit Product</title>", result[1])
        self.assertIn("<h1>Edit Product</h1>", result[1])
        self.assertIn('<button type="submit">Save</button>', result[1])

    def test_generate_html_create_pages_django_one_empty_class(self):
        # Edge case when one of the class in ModelsElement is somehow empty
        empty_class_object = ClassObject()
        self.models_elements.add_class(empty_class_object)
        result = generate_html_edit_pages_django(self.models_elements)
        self.assertEqual(len(result), 2)
        self.assertIn("<title>Edit Item</title>", result[0])
        self.assertIn("<title>Edit Product</title>", result[1])

    def test_generate_html_create_pages_django_multiple_class_same_name(self):
        # Edge case when some class in the ModelsElement somehow have the same
        # name, just return both HTML
        # It's an edge case because it is *supposed* to already be handled
        models_obj = ModelsElements("ModelTest")
        models_obj.add_class(self.class_object1)
        models_obj.add_class(self.class_object1)
        result = generate_html_edit_pages_django(models_obj)
        self.assertEqual(len(result), 2)
        self.assertIn("<title>Edit Item</title>", result[0])
        self.assertIn("<h1>Edit Item</h1>", result[0])
        self.assertIn("<title>Edit Item</title>", result[1])
        self.assertIn("<h1>Edit Item</h1>", result[1])
