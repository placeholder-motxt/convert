import os
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from app.generate_controller_springboot.generate_controller_springboot import (
    generate_springboot_controller_file,
    generate_springboot_controller_files,
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


class TestGenerateSpringbootControllerFiles(unittest.TestCase):
    def test_generate_springboot_controller_files_positive(self):
        # Arrange
        models_elements = MagicMock()
        class_object_1 = MagicMock()
        class_object_2 = MagicMock()

        # Set up mock behavior for models_elements
        models_elements.get_classes.return_value = [class_object_1, class_object_2]

        # Mock class names and public flags
        class_object_1.get_is_public.return_value = True
        class_object_1.get_name.return_value = "TestClass1"
        class_object_2.get_is_public.return_value = True
        class_object_2.get_name.return_value = "TestClass2"

        # Mock the method generate_springboot_controller_file
        with unittest.mock.patch(
            "app.generate_controller_springboot.generate_controller_springboot"
            ".generate_springboot_controller_file"
        ) as mock_generate_springboot_controller_file:
            mock_generate_springboot_controller_file.return_value = (
                "Controller 1"  # Mock the return value of this method
            )

            # Act
            result = generate_springboot_controller_files("hello", models_elements)

            # Assert
            self.assertEqual(len(result), 2)  # Expecting two controller files generated
            self.assertEqual(result[0], "Controller 1")
            self.assertEqual(result[1], "Controller 1")

    def test_generate_springboot_controller_files_no_class(self):
        models_elements = MagicMock()
        models_elements.get_classes.return_value = []
        result = generate_springboot_controller_files("hello", models_elements)
        self.assertEqual(len(result), 0)

    def test_generate_springboot_controller_files_no_public_class(self):
        # Arrange
        models_elements = MagicMock()
        class_object_1 = MagicMock()
        class_object_2 = MagicMock()

        # Set up mock behavior for models_elements
        models_elements.get_classes.return_value = [class_object_1, class_object_2]

        # Mock class names and public flags
        class_object_1.get_is_public.return_value = False
        class_object_2.get_is_public.return_value = False

        # Act
        result = generate_springboot_controller_files("hello", models_elements)

        # Assert
        self.assertEqual(
            len(result), 0
        )  # No public classes should result in empty list

    def test_generate_springboot_controller_files_empty_class_name(self):
        # Arrange
        models_elements = MagicMock()
        class_object_1 = MagicMock()

        # Set up mock behavior for models_elements
        models_elements.get_classes.return_value = [class_object_1]

        # Mock class names and public flags
        class_object_1.get_is_public.return_value = True
        class_object_1.get_name.return_value = ""  # Empty class name

        # Act
        result = generate_springboot_controller_files("hello", models_elements)

        # Assert
        self.assertEqual(result, [""])

    def test_generate_springboot_controller_files_handle_exception_in_rendering(self):
        # Arrange
        models_elements = MagicMock()
        class_object_1 = MagicMock()

        # Set up mock behavior for models_elements
        models_elements.get_classes.return_value = [class_object_1]

        # Mock class names and public flags
        class_object_1.get_is_public.return_value = True
        class_object_1.get_name.return_value = "TestClass1"

        # Mock rendering function to raise an exception
        with unittest.mock.patch(
            "app.generate_controller_springboot."
            "generate_controller_springboot.render_template",
            side_effect=Exception("Template error"),
        ):
            # Act
            result = generate_springboot_controller_files("hello", models_elements)
            # Assert
            self.assertEqual(len(result), 1)  # No file generated due to rendering error
