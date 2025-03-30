import unittest
from unittest.mock import MagicMock

from app.generate_frontend.create.generate_create_page_django import (
    generate_forms_create_page_django,
    generate_html_create_page_django,
    generate_html_create_pages_django,
)
from app.models.diagram import ClassObject, FieldObject
from app.models.elements import ModelsElements


class TestGenerateHtmlCreatePageDjango(unittest.TestCase):
    def setUp(self):
        # Setup a basic mock for the class object and fields.
        self.class_object = MagicMock(spec=ClassObject)
        self.field1 = MagicMock(spec=FieldObject)
        self.field2 = MagicMock(spec=FieldObject)
        self.field3 = MagicMock(spec=FieldObject)

        self.class_object.get_name.return_value = "Person"
        self.field1.get_name.return_value = "name"
        self.field2.get_name.return_value = "age"
        self.field3.get_name.return_value = "is_alive"

    def test_generate_html_create_page_django(self):
        # Test positive case for HTML page generation
        result = generate_html_create_page_django(self.class_object)
        self.assertIn(
            "Create Person", result
        )  # Checking if class name is correctly rendered

    def test_generate_html_create_page_django_empty_class(self):
        # Test negative case where the class is empty
        empty_class_object = MagicMock(spec=ClassObject)
        empty_class_object.get_name.return_value = ""  # No name for the class
        result = generate_html_create_page_django(empty_class_object)
        self.assertIn(r"<h1>Create  </h1>", result)  # No class name in the result


class TestGenerateHtmlCreatePagesDjango(unittest.TestCase):
    def setUp(self):
        # Setup a basic mock for the class object and fields.
        self.class_object = MagicMock(spec=ClassObject)
        self.field1 = MagicMock(spec=FieldObject)
        self.field2 = MagicMock(spec=FieldObject)
        self.field3 = MagicMock(spec=FieldObject)

        self.class_object.get_name.return_value = "Person"
        self.field1.get_name.return_value = "name"
        self.field2.get_name.return_value = "age"
        self.field3.get_name.return_value = "is_alive"

        # Create ModelsElements object with one class object
        self.models_elements = MagicMock(spec=ModelsElements)
        self.models_elements.get_classes.return_value = [self.class_object]
        self.class_object.get_fields.return_value = [
            self.field1,
            self.field2,
            self.field3,
        ]

    def test_generate_html_create_pages_django(self):
        # Test positive case for generating HTML pages for models elements
        result = generate_html_create_pages_django(self.models_elements)
        self.assertEqual(len(result), 1)  # One page should be generated
        self.assertIn("Create Person", result[0])

    def test_generate_html_create_pages_django_multiple_classes(self):
        # Test for multiple classes with same name
        self.models_elements.get_classes.return_value = [
            self.class_object,
            self.class_object,
        ]
        result = generate_html_create_pages_django(self.models_elements)
        self.assertEqual(len(result), 2)  # Two pages should be generated
        self.assertIn("Create Person", result[0])
        self.assertIn("Create Person", result[1])


class TestGenerateFormsCreatePageDjango(unittest.TestCase):
    def setUp(self):
        # Setup a basic mock for the class object and fields.
        self.class_object = MagicMock(spec=ClassObject)
        self.field1 = MagicMock(spec=FieldObject)
        self.field2 = MagicMock(spec=FieldObject)
        self.field3 = MagicMock(spec=FieldObject)

        self.class_object.get_name.return_value = "Person"
        self.field1.get_name.return_value = "name"
        self.field2.get_name.return_value = "age"
        self.field3.get_name.return_value = "is_alive"

        # Create ModelsElements object with one class object
        self.models_elements = MagicMock(spec=ModelsElements)
        self.models_elements.get_classes.return_value = [self.class_object]
        self.class_object.get_fields.return_value = [
            self.field1,
            self.field2,
            self.field3,
        ]

    def test_generate_forms_create_page_django(self):
        # Test positive case for form generation
        result = generate_forms_create_page_django(self.models_elements)

        # Checking the generated form class
        self.assertIn("class PersonForm(forms.ModelForm):", result)
        self.assertIn("name", result)  # Field names should appear in the form

    def test_generate_forms_create_page_django_no_fields(self):
        # Test case where the class has no fields
        self.class_object.get_fields.return_value = []  # Empty fields
        result = generate_forms_create_page_django(self.models_elements)
        self.assertIn("class PersonForm(forms.ModelForm):", result)
        self.assertIn("fields = []", result)  # No fields in the form

    def test_generate_forms_create_page_django_empty_class(self):
        # Test negative case where the class has no fields
        empty_class_object = MagicMock(spec=ClassObject)
        empty_class_object.get_name.return_value = "EmptyClass"
        empty_class_object.get_fields.return_value = []  # No fields
        empty_models_elements = MagicMock(spec=ModelsElements)
        empty_models_elements.get_classes.return_value = [empty_class_object]
        result = generate_forms_create_page_django(empty_models_elements)
        self.assertIn(
            "class EmptyClassForm(forms.ModelForm):", result
        )  # Form with no fields

    def test_generate_forms_create_page_django_no_class(self):
        # Test case with no classes in ModelsElements
        empty_models_elements = MagicMock(spec=ModelsElements)
        empty_models_elements.get_classes.return_value = []
        result = generate_forms_create_page_django(empty_models_elements)
        self.assertNotIn("Meta", result)


if __name__ == "__main__":
    unittest.main()
