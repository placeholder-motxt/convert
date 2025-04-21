import os
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from app.generate_controller_springboot.generate_controller_springboot import (
    generate_springboot_controller_file,
)

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestSequenceViewsJinja2Template(unittest.TestCase):
    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.to_pascal_case"
    )
    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.to_camel_case"
    )
    def test_generate_springboot_controller_file_positive(
        self, to_camel_case_mock: MagicMock, to_pascal_case_mock: MagicMock
    ):
        class_object = mock.Mock()
        class_object.get_name.return_value = "User"
        to_pascal_case_mock.return_value = "User"
        to_camel_case_mock.return_value = "user"

        with open(
            os.path.join(TEST_DIR, "generate_controller_springboot_positive.txt")
        ) as f:
            expected = f.read().strip()

        result = generate_springboot_controller_file("burhanpedia", class_object)
        self.assertEqual(result, expected)

    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.to_pascal_case"
    )
    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.to_camel_case"
    )
    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.render_template"
    )
    def test_generate_springboot_controller_file_negative(
        self,
        render_template_mock: MagicMock,
        to_camel_case_mock: MagicMock,
        to_pascal_case_mock: MagicMock,
    ):
        render_template_mock.side_effect = Exception("Test exception")
        class_object = mock.Mock()
        class_object.get_name.return_value = "User"
        to_pascal_case_mock.return_value = "User"
        to_camel_case_mock.return_value = "user"
        result = generate_springboot_controller_file("burhanpedia", class_object)
        self.assertEqual(result, "")

    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.to_pascal_case"
    )
    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.to_camel_case"
    )
    @patch(
        "app.generate_controller_springboot.generate_controller_springboot.render_template"
    )
    def test_generate_springboot_controller_file_empty_class_name(
        self,
        render_template_mock: MagicMock,
        to_camel_case_mock: MagicMock,
        to_pascal_case_mock: MagicMock,
    ):
        render_template_mock.side_effect = Exception("Test exception")
        class_object = mock.Mock()
        class_object.get_name.return_value = ""
        result = generate_springboot_controller_file("burhanpedia", class_object)
        self.assertEqual(result, "")
