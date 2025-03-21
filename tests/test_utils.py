import unittest
from unittest.mock import MagicMock, patch

import pytest

from app.utils import (  # Import the function from the module
    camel_to_snake,
    render_template,
)


class TestCamelToSnake(unittest.TestCase):
    # Positive Cases
    def test_single_word_camel_case(self):
        self.assertEqual(camel_to_snake("CamelCase"), "camel_case")

    def test_multiple_word_camel_case(self):
        self.assertEqual(camel_to_snake("CamelCaseNames"), "camel_case_names")

    def test_mixed_case_with_numbers(self):
        self.assertEqual(camel_to_snake("CamelCase123Names"), "camel_case123_names")

    def test_with_acronyms(self):
        self.assertEqual(camel_to_snake("CamelHTMLParser"), "camel_html_parser")

    # Negative Cases
    def test_with_not_string(self):
        with pytest.raises(TypeError):
            camel_to_snake(123)

    # Corner Cases

    def test_already_snake_case(self):
        self.assertEqual(camel_to_snake("snake_case"), "snake_case")

    def test_empty_string(self):
        self.assertEqual(camel_to_snake(""), "")

    def test_only_uppercase_letter(self):
        self.assertEqual(camel_to_snake("A"), "a")

    def test_only_lowercase(self):
        self.assertEqual(camel_to_snake("lowercase"), "lowercase")

    def test_numbers_in_camel_case(self):
        self.assertEqual(camel_to_snake("Camel123Case"), "camel123_case")

    def test_mixed_case_with_numbers_and_underscores(self):
        self.assertEqual(camel_to_snake("Camel123_CaseName"), "camel123_case_name")

    def test_single_character(self):
        self.assertEqual(camel_to_snake("X"), "x")


class TestRenderTemplate(unittest.TestCase):
    @patch("app.utils.env.get_template")  # Mock the jinja2 environment
    def test_render_valid_template(self, mock_get_template: MagicMock):
        """Test case for rendering a valid template."""
        # Arrange
        mock_template = MagicMock()
        mock_template.render.return_value = "Rendered Output"
        mock_get_template.return_value = mock_template

        context = {"key": "value"}
        result = render_template("valid_template.html", context)

        # Assert
        mock_get_template.assert_called_once_with("valid_template.html")
        mock_template.render.assert_called_once_with(context)
        self.assertEqual(result, "Rendered Output")

    def test_render_invalid_template(self):
        """Test case when the template does not exist."""
        # Arrange
        with patch("app.utils.env.get_template") as mock_get_template:
            mock_get_template.side_effect = Exception("Template not found")

            # Act
            result = render_template("invalid_template.html", {"key": "value"})

            # Assert
            self.assertEqual(result, "")

    def test_render_template_with_invalid_context(self):
        """Test case when the context is invalid."""
        # Arrange
        with patch("app.utils.env.get_template") as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.side_effect = Exception("Invalid context")
            mock_get_template.return_value = mock_template

            # Act
            result = render_template(
                "valid_template.html", {"invalid_key": "invalid_value"}
            )

            # Assert
            mock_get_template.assert_called_once_with("valid_template.html")
            mock_template.render.assert_called_once_with(
                {"invalid_key": "invalid_value"}
            )
            self.assertEqual(result, "")

    def test_render_empty_context(self):
        """Test case when the context is empty."""
        # Arrange
        with patch("app.utils.env.get_template") as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.return_value = "Rendered with empty context"
            mock_get_template.return_value = mock_template

            # Act
            result = render_template("valid_template.html", {})

            # Assert
            self.assertEqual(result, "Rendered with empty context")

    def test_render_template_with_keywords_in_context(self):
        """Test case with Python keywords in context."""
        # Arrange
        with patch("app.utils.env.get_template") as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.return_value = "Rendered with keyword context"
            mock_get_template.return_value = mock_template

            context = {"if": "keyword_value"}  # 'if' is a Python keyword
            # Act
            result = render_template("valid_template.html", context)

            # Assert
            self.assertEqual(result, "Rendered with keyword context")

    def test_render_empty_template(self):
        """Test case when the template is empty."""
        # Arrange
        with patch("app.utils.env.get_template") as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.return_value = ""
            mock_get_template.return_value = mock_template
            # Act
            result = render_template("empty_template.html", {})
            # Assert
            self.assertEqual(result, "")
