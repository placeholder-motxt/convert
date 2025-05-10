import os
import unittest
from pathlib import Path
from unittest import mock

from app.models.diagram import ClassObject
from app.models.elements import (
    DependencyElements,
    ModelsElements,
    RequirementsElements,
    UrlsElement,
    ViewsElements,
)

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestModelsElements(unittest.TestCase):
    def test_models_elements_valid_filename(self):
        obj = ModelsElements("model_file.py")
        self.assertIsInstance(obj, ModelsElements)

    def test_models_elements_invalid_filename_type(self):
        with self.assertRaises(TypeError):
            ModelsElements(123)  # Invalid type

    def test_models_elements_empty_filename(self):  # cornercase
        with self.assertRaises(ValueError):
            ModelsElements("")

    def test_parse(self):
        obj = ModelsElements("string")
        with mock.patch("app.models.elements.ParseJsonToObjectClass") as mock_parser:
            mock_parser_instance = mock_parser.return_value
            mock_parser_instance.parse_classes.return_value = [mock.Mock()]

            self.assertEqual(
                obj.parse("content"), mock_parser_instance.parse_classes.return_value
            )

    def test_print_django_style(self):
        obj = ModelsElements("models.py")
        obj.parse(open("tests/test_input.txt", "r").read())
        res = obj.print_django_style()
        f = open("tests/test_result.txt", "r")
        self.assertEqual(res, f.read())

    def test_add_class_positive_case(self):
        """Test: Positive case where a valid ClassObject is added."""
        self.models = ModelsElements("test_file")
        class_obj = ClassObject()
        class_obj.set_name("TestClass")
        self.models.add_class(class_obj)

        # Assert that the class has been added correctly
        classes = self.models.get_classes()
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].get_name(), "TestClass")

    def test_add_class_negative_case_invalid_type(self):
        """Test: Negative case where a non-ClassObject is added."""
        self.models = ModelsElements("test_file")
        with self.assertRaises(ValueError):
            self.models.add_class("InvalidClassObject")

    def test_add_class_corner_case_empty_class(self):
        """Test: Corner case where an empty ClassObject (no name or minimal attributes) is added."""
        self.models = ModelsElements("test_file")
        empty_class_obj = ClassObject()
        self.models.add_class(empty_class_obj)

        # Assert that the empty class object has been added correctly
        classes = self.models.get_classes()
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].get_name(), "")

    def test_add_class_corner_case_multiple_classes(self):
        """Test: Corner case where multiple valid ClassObjects are added."""
        self.models = ModelsElements("test_file")
        class_obj_1 = ClassObject()
        class_obj_1.set_name("Class1")
        class_obj_2 = ClassObject()
        class_obj_2.set_name("Class2")
        self.models.add_class(class_obj_1)
        self.models.add_class(class_obj_2)

        # Assert that multiple classes can be added and accessed
        classes = self.models.get_classes()
        self.assertEqual(len(classes), 2)
        self.assertEqual(classes[0].get_name(), "Class1")
        self.assertEqual(classes[1].get_name(), "Class2")

    def test_add_class_corner_case_same_class_multiple_times(self):
        """Test: Corner case where the same ClassObject is added multiple times."""
        self.models = ModelsElements("test_file")
        class_obj = ClassObject()
        class_obj.set_name("DuplicateClass")
        self.models.add_class(class_obj)
        self.models.add_class(class_obj)

        # Assert that the class object can be added multiple times (no restrictions on duplicates)
        classes = self.models.get_classes()
        self.assertEqual(len(classes), 2)
        self.assertEqual(classes[0].get_name(), "DuplicateClass")
        self.assertEqual(classes[1].get_name(), "DuplicateClass")

    def test_composition_one_to_many(self):
        self.maxDiff = None
        data = ""
        with open(os.path.join(TEST_DIR, "test_composition1.json")) as f:
            data = f.read()

        expected = ""
        with open(os.path.join(TEST_DIR, "test_composition_result1.txt")) as f:
            expected = f.read()

        model = ModelsElements("test_composition")
        model.parse(data)
        res = model.print_django_style()
        self.assertEqual(res, expected)

    def test_composition_many_to_one(self):
        self.maxDiff = None
        data = ""
        with open(os.path.join(TEST_DIR, "test_composition2.json")) as f:
            data = f.read()

        expected = ""
        with open(os.path.join(TEST_DIR, "test_composition_result2.txt")) as f:
            expected = f.read()

        model = ModelsElements("test_composition")
        model.parse(data)
        res = model.print_django_style()
        self.assertEqual(res, expected)

    def test_composition_one_to_many_template(self):
        self.maxDiff = None
        data = ""
        with open(os.path.join(TEST_DIR, "test_composition1.json")) as f:
            data = f.read()

        expected = ""
        with open(os.path.join(TEST_DIR, "test_composition_result_template1.txt")) as f:
            expected = f.read()

        model = ModelsElements("test_composition")
        model.parse(data)
        res = model.print_django_style_template()
        self.assertEqual(res, expected)

    def test_composition_many_to_one_template(self):
        self.maxDiff = None
        data = ""
        with open(os.path.join(TEST_DIR, "test_composition2.json")) as f:
            data = f.read()

        expected = ""
        with open(os.path.join(TEST_DIR, "test_composition_result_template2.txt")) as f:
            expected = f.read()

        model = ModelsElements("test_composition")
        model.parse(data)
        res = model.print_django_style_template()
        self.assertEqual(res, expected)


class TestViewsElements(unittest.TestCase):
    def setUp(self):
        self.views_elements = ViewsElements("view_file.py")

    def test_instance_of_file_elements(self):
        self.assertIsInstance(self.views_elements, ViewsElements)

    def test_print_django_style_no_methods(self):
        expected_output = ""
        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_one_controller_method(self):
        mock_controller_method = mock.Mock()
        mock_controller_method.print_django_style.return_value = (
            "def sample_controller(request):\n\tpass\n"
        )
        self.views_elements.add_controller_method(mock_controller_method)
        expected_output = "def sample_controller(request):\n\tpass\n"
        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_multiple_controller_methods(self):
        mock_controller_method1 = mock.Mock()
        mock_controller_method1.print_django_style.return_value = (
            "def controller_one(request):\n\tpass\n"
        )
        mock_controller_method2 = mock.Mock()
        mock_controller_method2.print_django_style.return_value = (
            "def controller_two(request):\n\tpass\n"
        )

        self.views_elements.add_controller_method(mock_controller_method1)
        self.views_elements.add_controller_method(mock_controller_method2)

        expected_output = (
            "def controller_one(request):\n"
            "\tpass\n"
            "def controller_two(request):\n"
            "\tpass\n"
        )

        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_class_methods(self):
        mock_class_method_1 = mock.Mock()
        mock_class_method_1.get_name.return_value = "Class1"
        mock_class_method_1.to_views_code.return_value = (
            "def class_method():\n\tmethod_call = inner_method1(arg1, arg2)"
        )
        mock_class_method_2 = mock.Mock()
        mock_class_method_2.get_name.return_value = "Class2"
        mock_class_method_2.to_views_code.return_value = (
            "def class_method():\n\tmethod_call = inner_method2(arg1, arg2)"
        )
        self.views_elements.add_class_method(mock_class_method_1)
        self.views_elements.add_class_method(mock_class_method_2)
        self.assertEqual(
            self.views_elements.print_django_style(),
            (
                "#-----method from class Class1------\n\n"
                "def class_method():\n"
                "\tmethod_call = inner_method1(arg1, arg2)\n\n\n"
                "#-----method from class Class2------\n\n"
                "def class_method():\n"
                "\tmethod_call = inner_method2(arg1, arg2)\n\n\n"
            ),
        )

    def test_print_django_style_with_one_class_method(self):
        mock_class_method_1 = mock.Mock()
        mock_class_method_1.get_name.return_value = "Class1"
        mock_class_method_1.to_views_code.return_value = (
            "def class_method():\n\tmethod_call = inner_method1(arg1, arg2)"
        )
        self.views_elements.add_class_method(mock_class_method_1)
        self.assertEqual(
            self.views_elements.print_django_style(),
            (
                "#-----method from class Class1------\n\n"
                "def class_method():\n"
                "\tmethod_call = inner_method1(arg1, arg2)\n\n\n"
            ),
        )


class TestUrlsElements(unittest.IsolatedAsyncioTestCase):
    def test_print_django_style(self):
        self.requirements_elements = UrlsElement("urls.py")
        mock_class = mock.Mock()
        mock_class.get_name.return_value = "Class1"
        mock_class.get_is_public.return_value = True
        self.requirements_elements.set_classes(classes=[mock_class])
        res = self.requirements_elements.print_django_style()
        self.assertEqual(
            res,
            '"""\n'
            "This code is generated using MoTxT,\n"
            "checkout more about us on https://motxt.ppl.cs.ui.ac.id\n"
            '"""\n\n'
            "from django.urls import path\n"
            "from .views import (\n    "
            "landing_page,\n    "
            "create_class1,\n    "
            "get_class1,\n    "
            "edit_class1,\n    "
            "delete_class1,\n    "
            ")\n\n"
            'app_name = "main"\n\n'
            "urlpatterns = [\n    "
            "path('', landing_page , name=\"landing_page\"),\n    "
            "path('create-class1/', create_class1, name=\"create_class1\"),\n    "
            "path('get-all-class1/', get_class1, name=\"get_class1\"),\n    "
            "path('edit-class1/<int:id>/', edit_class1, name=\"edit_class1\"),\n    "
            "path('delete-class1/', delete_class1, name=\"delete_class1\"),\n]",
        )

    async def test_write_to_file(self):
        self.requirements_elements = UrlsElement("urls.py")
        mock_class = mock.Mock()
        mock_class.get_name.return_value = "Class1"
        await self.requirements_elements.write_to_file(path="./tests")
        print(Path("./tests/urls.py").is_file())
        self.assertTrue(Path("./tests/urls.py").is_file())
        if Path("./tests/urls.py").is_file():
            os.remove("./tests/urls.py")


class TestRequirementsElements(unittest.IsolatedAsyncioTestCase):
    def test_print_django_style(self):
        self.requirements_elements = RequirementsElements("requirements.txt")
        res = self.requirements_elements.print_django_style()
        self.assertEqual(
            res,
            "Django\n"
            "gunicorn\n"
            "whitenoise\n"
            "psycopg2-binary\n"
            "pytest\n"
            "pytest-django\n"
            "pytest-cov\n",
        )

    async def test_write_to_file(self):
        self.requirements_elements = RequirementsElements("requirements.txt")
        await self.requirements_elements.write_to_file("./app")
        self.assertTrue(Path("./app/requirements.txt").is_file())
        if Path("./app/requirements.txt").is_file():
            os.remove("./app/requirements.txt")


class TestDependencyElements(unittest.TestCase):
    def setUp(self):
        self.dependency_elements = DependencyElements("build.gradle.kts")

    def test_print_springboot_style_positive_case(self):
        """Test: Positive case where valid project name is provided."""
        project_name = "MySpringBootApp"
        result = self.dependency_elements.print_springboot_style(project_name)
        self.assertIn("MySpringBootApp", result)
        self.assertIn("org.springframework.boot:spring-boot-starter-web", result)
        self.assertIn("mavenCentral()", result)

    def test_print_springboot_style_negative_case_empty_project_name(self):
        """Test: Negative case where an empty project name is provided."""
        project_name = ""
        with self.assertRaises(Exception) as e:
            self.dependency_elements.print_springboot_style(project_name)
        self.assertEqual(
            str(e.exception), "Error rendering template: Project name cannot be empty!"
        )

    def test_print_springboot_style_edge_case_long_project_name(self):
        """Test: Edge case where a very long project name is provided."""
        project_name = "A" * 1000  # Very long project name
        result = self.dependency_elements.print_springboot_style(project_name)
        self.assertIn("A" * 1000, result)
        self.assertIn("org.springframework.boot:spring-boot-starter-web", result)

    def test_print_springboot_style_edge_case_special_characters_in_project_name(self):
        """Test: Edge case where project name contains special characters."""
        project_name = "My@Spring#Boot$App!"
        result = self.dependency_elements.print_springboot_style(project_name)
        self.assertIn("My@Spring#Boot$App!", result)
        self.assertIn("org.springframework.boot:spring-boot-starter-web", result)

    def test_print_application_properties(self):
        """Test: Check if the application.properties file is created correctly."""
        result = self.dependency_elements.print_application_properties()
        expected_output = (
            "springdoc.api-docs.enabled=true\n"
            + "springdoc.swagger-ui.enabled=true\n"
            + "spring.datasource.url=jdbc:sqlite:mydatabase.db\n"
            + "spring.datasource.driver-class-name=org.sqlite.JDBC\n"
            + "spring.jpa.show-sql=true\n"
            + "spring.jpa.database-platform=org.hibernate.community.dialect.SQLiteDialect\n"
            + "spring.jpa.hibernate.ddl-auto=update\n"
        )
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
