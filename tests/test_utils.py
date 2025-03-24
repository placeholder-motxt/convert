import unittest

from app.utils import camel_to_snake  # Import the function from the module


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
    def test_already_snake_case(self):
        self.assertEqual(camel_to_snake("snake_case"), "snake_case")

    def test_empty_string(self):
        self.assertEqual(camel_to_snake(""), "")

    def test_only_uppercase_letter(self):
        self.assertEqual(camel_to_snake("A"), "a")

    # Corner Cases
    def test_only_lowercase(self):
        self.assertEqual(camel_to_snake("lowercase"), "lowercase")

    def test_numbers_in_camel_case(self):
        self.assertEqual(camel_to_snake("Camel123Case"), "camel123_case")

    def test_mixed_case_with_numbers_and_underscores(self):
        self.assertEqual(camel_to_snake("Camel123_CaseName"), "camel123_case_name")

    def test_single_character(self):
        self.assertEqual(camel_to_snake("X"), "x")
