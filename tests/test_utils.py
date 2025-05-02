import keyword
import unittest
from typing import Any, Type
from unittest.mock import MagicMock, patch

import pytest

from app.utils import (  # Import the function from the module
    camel_to_snake,
    is_valid_java_identifier,
    render_template,
    to_camel_case,
    to_pascal_case,
    translate_to_cat,
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


class TestToCamelCase(unittest.TestCase):
    def test_regular_case(self):
        self.assertEqual(
            to_camel_case("hello world example string"), "helloWorldExampleString"
        )

    def test_case_with_underscores(self):
        self.assertEqual(
            to_camel_case("hello_world_example_string"), "helloWorldExampleString"
        )

    def test_case_with_hyphens(self):
        self.assertEqual(
            to_camel_case("hello-world-example-string"), "helloWorldExampleString"
        )

    def test_mixed_case_input(self):
        self.assertEqual(
            to_camel_case("HeLLo WoRLd ExaMplE String"), "helloWorldExampleString"
        )

    def test_no_special_characters(self):
        self.assertEqual(to_camel_case("helloWorld"), "helloWorld")

    def test_leading_trailing_spaces(self):
        self.assertEqual(
            to_camel_case("  hello world example string  "), "helloWorldExampleString"
        )

    def test_multiple_spaces_between_words(self):
        self.assertEqual(
            to_camel_case("hello    world      example    string"),
            "helloWorldExampleString",
        )

    def test_empty_string(self):
        self.assertEqual(to_camel_case(""), "")

    def test_single_word(self):
        self.assertEqual(to_camel_case("hello"), "hello")

    def test_non_alphanumeric_characters(self):
        self.assertEqual(to_camel_case("!@#$%^&*()_+"), "")

    def test_random_non_alphanumeric_characters(self):
        self.assertEqual(to_camel_case("$$$hello###world$$$"), "helloWorld")


class TestErrorClassification(unittest.TestCase):
    def test_error_categories(self):
        test_cases = [
            ("Project name must not contain whitespace or number", "invalid_project"),
            ("App name must not contain whitespace", "invalid_project"),
            ("File MyProject.zip does not exist", "missing_file"),
            (
                "Cannot call class 'UserController' objects not defined in Class Diagram!",
                "undefined_class",
            ),
            ("Error: Invalid JSON format", "invalid_class_file"),
            (
                "Nodes not found in the json, \nplease make sure the file isn't corrupt",
                "invalid_class_file",
            ),
            (
                "Class not found in the json, \nplease make sure the file isn't corrupt",
                "invalid_class_file",
            ),
            ("ModelsElements does not contain any classes", "invalid_class_file"),
            ("Can't create edit views with no class", "invalid_class_file"),
            ("The .sequence.jet is not valid", "invalid_sequence_file"),
            (
                "please consult the user manual document on how to name classes",
                "invalid_class_name",
            ),
            (
                "Method return type not found, \nplease add a return type for method save",
                "invalid_method_return",
            ),
            ("method name or method return type name", "invalid_method_return"),
            (
                "please consult the user manual document on how to name return variables",
                "invalid_return_variable",
            ),
            ("Too deep self calls on a sequence diagram", "too_many_self_call"),
            ("Invalid param name", "invalid_param_name"),
            ("Parameter name please consult the user", "invalid_param_name"),
            (
                "please consult the user manual document on how to name parameters",
                "invalid_param_name",
            ),
            ("Error: attribute name or type is not valid", "invalid_attribute_name"),
            (
                "Return edge label must be a valid variable name!",
                "invalid_attribute_name",
            ),
            (
                "please consult the user manual document on how to name parameter types",
                "invalid_param_type",
            ),
            (
                "Return edge must have a corresponding call edge on sequence diagram",
                "no_call_edge",
            ),
            ("Association multiplicity is empty on relation", "invalid_relation"),
            ("Invalid use of * in multiplicity on relation", "invalid_relation"),
            ("Relationship in class diagram is wrong", "invalid_relation"),
            ("Invalid multiplicity on relationship", "invalid_relation"),
            (
                "please consult the user manual document on how to name methods",
                "invalid_method_name",
            ),
            ("method cannot be empty", "invalid_method_name"),
            ("ClassMethodObject cannot be SET to be None", "invalid_method_name"),
            (
                "Duplicate class name 'AccountService' on sequence diagram",
                "duplicate_class",
            ),
            ("instance_name cannot be empty", "invalid_instance_name"),
            ("please remove one of the parameters", "duplicate_attribute"),
            ("Something unexpected", "other"),  # unmatched case
        ]

        for message, expected_category in test_cases:
            with self.subTest(msg=message):
                category = translate_to_cat(message)
                self.assertEqual(category, expected_category)


class TestToPascalCase(unittest.TestCase):
    def test_basic_cases(self):
        self.assertEqual(to_pascal_case("hello_world"), "HelloWorld")
        self.assertEqual(to_pascal_case("convert-to-pascal"), "ConvertToPascal")
        self.assertEqual(
            to_pascal_case("multiple words with spaces"), "MultipleWordsWithSpaces"
        )

    def test_acronym_handling(self):
        self.assertEqual(to_pascal_case("api_response"), "APIResponse")
        self.assertEqual(to_pascal_case("get_http_status"), "GetHTTPStatus")
        self.assertEqual(to_pascal_case("parse_xml_data"), "ParseXMLData")
        self.assertEqual(to_pascal_case("user_id"), "UserID")

    def test_custom_acronym_set(self):
        acronyms = {"DB", "SQL"}
        self.assertEqual(to_pascal_case("connect_to_db", acronyms), "ConnectToDB")
        self.assertEqual(to_pascal_case("run_sql_query", acronyms), "RunSQLQuery")

    def test_edge_cases(self):
        self.assertEqual(to_pascal_case(""), "")
        self.assertEqual(to_pascal_case("    "), "")
        self.assertEqual(
            to_pascal_case("alreadyPascalCase"), "Alreadypascalcase"
        )  # no detection of existing PascalCase
        self.assertEqual(to_pascal_case("123number_test"), "123numberTest")


class TestIsValidJavaIdentifier(unittest.TestCase):
    """All methods here follow the one-assertion-per-test rule."""

    # ── positive samples ───────────────────────────────────────────────────────
    _positive_cases: dict[str, str] = {
        "single_lower": "a",
        "single_upper": "Z",
        "underscore_only": "_",
        "dollar_only": "$",
        "camelCase": "camelCase",
        "leading_underscore": "_privateVar",
        "leading_dollar": "$generated",
        "alphanumeric": "var123",
        "non_ascii": "Éclair",
        "very_long": "a" * 1000,
    }

    # ── negative samples ────────────────────────────────────────────────────────
    _negative_cases: dict[str, str] = {
        "keyword_class": "class",
        "keyword_for": "for",
        "keyword_while": "while",
        "starts_with_digit": "1stPlace",
        "digit_only": "9",
        "hyphen": "contains-hyphen",
        "space": "white space",
        "tab": "tab\tchar",
        "newline": "newline\n",
        "asterisk": "a*b",
        "hash": "hash#tag",
        "emoji": "smile😊",
    }

    # ── edge / exceptional samples ─────────────────────────────────────────────
    _raises_cases: dict[str, tuple[Any, Type[Exception]]] = {
        "empty_string": ("", IndexError),
        "none_input": (None, TypeError),  # type: ignore[arg-type]
    }


# ── helpers that add *typed* one-assertion tests ──────────────────────────────
def _add_bool_test(cls: type, name: str, identifier: str, expected: bool) -> None:
    def _test(
        self: unittest.TestCase, identifier: str = identifier, expected: bool = expected
    ) -> None:
        self.assertEqual(is_valid_java_identifier(identifier), expected)

    _test.__name__ = f"test_{name}"
    setattr(cls, _test.__name__, _test)


def _add_raises_test(
    cls: type,
    name: str,
    identifier: Any,  # noqa: ANN401
    exc: Type[Exception],
) -> None:
    def _test(
        self: unittest.TestCase,
        identifier: Any = identifier,  # noqa: ANN401
        exc: Type[Exception] = exc,
    ) -> None:
        with self.assertRaises(exc):
            is_valid_java_identifier(identifier)  # type: ignore[arg-type]

    _test.__name__ = f"test_{name}"
    setattr(cls, _test.__name__, _test)


# positive cases
for _name, _ident in TestIsValidJavaIdentifier._positive_cases.items():
    _add_bool_test(TestIsValidJavaIdentifier, f"valid_{_name}", _ident, True)

# negative cases
for _name, _ident in TestIsValidJavaIdentifier._negative_cases.items():
    _add_bool_test(TestIsValidJavaIdentifier, f"invalid_{_name}", _ident, False)

# each Python keyword becomes its own single-assert test
for _kw in keyword.kwlist:
    _add_bool_test(TestIsValidJavaIdentifier, f"keyword_{_kw}", _kw, False)

# edge / exception cases
for _name, (_ident, _exc) in TestIsValidJavaIdentifier._raises_cases.items():
    _add_raises_test(TestIsValidJavaIdentifier, f"raises_{_name}", _ident, _exc)


if __name__ == "__main__":
    unittest.main()
