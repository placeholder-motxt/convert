import unittest
from unittest.mock import MagicMock, patch

from app.generate_frontend.read.read_page_views import generate_read_page_views
from app.models.elements import ClassObject, ModelsElements


class TestGenerateReadPageViews(unittest.TestCase):
    @patch("app.generate_frontend.read.read_page_views.render_template")
    def test_generate_read_page_views_positive(self, mock_render_template: MagicMock):
        """Positive case: Valid classes in ModelsElements render correct context."""
        # Create a ModelsElements instance with some classes
        models_elements = ModelsElements("test_file")
        class_obj1 = ClassObject()
        class_obj1.set_name("Person")
        class_obj1.set_is_public(True)
        class_obj2 = ClassObject()
        class_obj2.set_name("Vehicle")
        class_obj2.set_is_public(True)
        models_elements.add_class(class_obj1)
        models_elements.add_class(class_obj2)

        expected_context = {
            "classes": [
                {"class_name": "Person", "class_snake": "person"},
                {"class_name": "Vehicle", "class_snake": "vehicle"},
            ]
        }

        # Simulate the render_template function to return a dummy string.
        mock_render_template.return_value = "Rendered Read Page Views"
        result = generate_read_page_views(models_elements)

        mock_render_template.assert_called_once_with(
            "read_page_views.py.j2", expected_context
        )
        self.assertEqual(result, "Rendered Read Page Views")

    @patch("app.generate_frontend.read.read_page_views.render_template")
    def test_generate_read_page_views_corner_no_classes(
        self, mock_render_template: MagicMock
    ):
        """Negative case: When no classes exist, the result should still be generated."""
        models_elements = ModelsElements("test_file")

        # Empty context since no classes are added.
        expected_context = {"classes": []}

        mock_render_template.return_value = "Rendered Empty Read Page Views"
        result = generate_read_page_views(models_elements)

        mock_render_template.assert_called_once_with(
            "read_page_views.py.j2", expected_context
        )
        self.assertEqual(result, "Rendered Empty Read Page Views")

    def test_generate_read_page_views_negative_type_error(self):
        """Test case: Check for TypeError when invalid type is passed."""
        with self.assertRaises(TypeError) as context:
            generate_read_page_views("InvalidType")
        self.assertEqual(
            str(context.exception),
            "Expected type ModelsElements, got <class 'str'> instead",
        )

    @patch("app.generate_frontend.read.read_page_views.render_template")
    def test_generate_read_page_views_corner_empty_class_name(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Empty class name."""
        models_elements = ModelsElements("test_file")
        class_obj1 = ClassObject()
        class_obj1.set_name("")  # Empty class name
        class_obj1.set_is_public(True)

        models_elements.add_class(class_obj1)

        expected_context = {"classes": [{"class_name": "", "class_snake": ""}]}

        mock_render_template.return_value = "Rendered Empty Class Name Read Page Views"
        result = generate_read_page_views(models_elements)

        mock_render_template.assert_called_once_with(
            "read_page_views.py.j2", expected_context
        )
        self.assertEqual(result, "Rendered Empty Class Name Read Page Views")

    @patch("app.generate_frontend.read.read_page_views.render_template")
    def test_generate_read_page_views_corner_special_characters_in_class_name(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Class names with special characters."""
        models_elements = ModelsElements("test_file")
        class_obj1 = ClassObject()
        class_obj1.set_name("Test-Class")  # Class name with hyphen
        class_obj1.set_is_public(True)

        models_elements.add_class(class_obj1)

        expected_context = {
            "classes": [{"class_name": "Test-Class", "class_snake": "test-class"}]
        }

        mock_render_template.return_value = (
            "Rendered Special Character Class Read Page Views"
        )
        result = generate_read_page_views(models_elements)

        mock_render_template.assert_called_once_with(
            "read_page_views.py.j2", expected_context
        )
        self.assertEqual(result, "Rendered Special Character Class Read Page Views")

    @patch("app.generate_frontend.read.read_page_views.render_template")
    def test_generate_read_page_views_corner_large_number_of_classes(
        self, mock_render_template: MagicMock
    ):
        """Corner case: Large number of classes."""
        models_elements = ModelsElements("test_file")
        num_classes = 100
        expected_context = {"classes": []}

        # Add a large number of classes with unique names
        for i in range(num_classes):
            class_obj = ClassObject()
            class_obj.set_name(f"Class{i}")
            class_obj.set_is_public(True)
            models_elements.add_class(class_obj)
            expected_context["classes"].append(
                {"class_name": f"Class{i}", "class_snake": f"class{i}"}
            )

        mock_render_template.return_value = (
            "Rendered Large Number of Classes Page Views"
        )
        result = generate_read_page_views(models_elements)

        mock_render_template.assert_called_once_with(
            "read_page_views.py.j2", expected_context
        )
        self.assertEqual(result, "Rendered Large Number of Classes Page Views")
