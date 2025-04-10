import json
import os
import shutil
import unittest
import zipfile

from app.generate_frontend.create.generate_create_page_django import (
    generate_html_create_pages_django,
)
from app.main import (
    fetch_data,
    generate_file_to_be_downloaded,
    get_names_from_classes,
)
from app.models.elements import RequirementsElements, UrlsElement


class TestGenerateFileToBeDownloadedPrivate(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and switch to it.
        with open("tests/testdata/input_generate_file_to_be_downloaded.json", "r") as f:
            json_data = json.load(f)
        self.filename = json_data["filename"]
        self.content = json_data["content"]
        data = fetch_data(self.filename, self.content)
        writer_requirements = RequirementsElements("requirements.txt")
        writer_urls = UrlsElement("urls.py")
        # simulate the creation of requirements.txt and urls.py instead of using write_to_file()
        with open(os.path.join(os.getcwd(), "app", "requirements.txt"), "w") as f:
            f.write(writer_requirements.print_django_style())

        self.models_content = data["models"]
        self.views_content = data["views"]
        self.writer_models = data["model_element"]
        self.project_name = self.filename[0]
        writer_urls.set_classes(self.writer_models.get_classes())
        with open(os.path.join(os.getcwd(), "app", "urls.py"), "w") as f:
            f.write(writer_urls.print_django_style())

    def test_generate_file_to_be_downloaded(self):
        result = generate_file_to_be_downloaded(
            self.project_name,
            self.models_content,
            self.views_content,
            self.writer_models,
        )

        # Expected output in the zip file.
        expected_output = [
            "file1/asgi.py",
            "manage.py",
            "file1/settings.py",
            "file1/urls.py",
            "file1/wsgi.py",
            "main/admin.py",
            "main/apps.py",
            "main/models.py",
            "main/tests.py",
            "main/views.py",
            "main/migrations/__init__.py",
            "main/templatetags/__init__.py",
            "main/templatetags/filter_tag.py",
            "main/__init__.py",
            "requirements.txt",
            "main/urls.py",
            "run.sh",
            "run.bat",
            "main/forms.py",
            "main/templates/landing_page.html",
            "templates/base.html",
        ]
        for path in expected_output:
            self.assertIn(path, result)
        with zipfile.ZipFile(f"{self.project_name}.zip", "r") as zipf:
            for file in zipf.namelist():
                self.assertIn(file, expected_output)

    def test_generate_file_to_be_downloaded_without_requirements(self):
        if os.path.exists(os.path.join(os.getcwd(), "app", "requirements.txt")):
            os.remove(os.path.join(os.getcwd(), "app", "requirements.txt"))
        with self.assertRaises(FileNotFoundError) as ctx:
            generate_file_to_be_downloaded(
                self.project_name,
                self.models_content,
                self.views_content,
                self.writer_models,
            )
        self.assertEqual(
            str(ctx.exception),
            "File requirements.txt does not exist",
        )

    def test_generate_file_to_be_downloaded_without_urls(self):
        if os.path.exists(os.path.join(os.getcwd(), "app", "urls.py")):
            os.remove(os.path.join(os.getcwd(), "app", "urls.py"))
        with self.assertRaises(FileNotFoundError) as ctx:
            generate_file_to_be_downloaded(
                self.project_name,
                self.models_content,
                self.views_content,
                self.writer_models,
            )
        self.assertEqual(
            str(ctx.exception),
            "File urls.py does not exist",
        )

    def test_generate_file_to_be_downloaded_multiple_calls(self):
        """
        Call generate_file_to_be_downloaded() twice in a row to ensure that the function
        cleans up previous zip files and project directories properly.
        """
        # First call: generate the file
        result_first = generate_file_to_be_downloaded(
            self.project_name,
            self.models_content,
            self.views_content,
            self.writer_models,
        )
        self.assertTrue(os.path.exists(f"{self.project_name}.zip"))
        with zipfile.ZipFile(f"{self.project_name}.zip", "r") as zipf:
            content_first = zipf.namelist()
        # Store the file list from the first generation.
        expected_files_first = set(result_first)

        # Second call: generate the file again with the same parameters.
        result_second = generate_file_to_be_downloaded(
            self.project_name,
            self.models_content,
            self.views_content,
            self.writer_models,
        )
        self.assertTrue(os.path.exists(f"{self.project_name}.zip"))
        with zipfile.ZipFile(f"{self.project_name}.zip", "r") as zipf:
            content_second = zipf.namelist()
        # Ensure that both generated outputs are the same.
        expected_files_second = set(result_second)
        self.assertEqual(set(content_first), expected_files_second)
        self.assertEqual(set(content_second), expected_files_first)

    def tearDown(self):
        # Remove any created zip file or project folder.
        if os.path.exists(f"{self.project_name}.zip"):
            os.remove(f"{self.project_name}.zip")
        if os.path.exists(f"project_{self.project_name}"):
            shutil.rmtree(f"project_{self.project_name}")
        if os.path.exists(f"{self.project_name}_models.py"):
            os.remove(f"{self.project_name}_models.py")
        if os.path.exists(f"{self.project_name}_views.py"):
            os.remove(f"{self.project_name}_views.py")
        if os.path.exists(os.path.join(os.getcwd(), "app", "requirements.txt")):
            os.remove(os.path.join(os.getcwd(), "app", "requirements.txt"))
        if os.path.exists(os.path.join(os.getcwd(), "app", "urls.py")):
            os.remove(os.path.join(os.getcwd(), "app", "urls.py"))


class TestGenerateFileToBeDownloadedPublic(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory (if needed) and load test input.
        with open(
            "tests/testdata/input_generate_file_to_be_downloaded_public.json", "r"
        ) as f:
            json_data = json.load(f)
        self.filename = json_data["filename"]
        self.content = json_data["content"]
        self.project_name = json_data["project_name"]
        data = fetch_data(self.filename, self.content)
        writer_requirements = RequirementsElements("requirements.txt")
        writer_urls = UrlsElement("urls.py")
        # simulate the creation of requirements.txt and urls.py instead of using write_to_file()
        with open(os.path.join(os.getcwd(), "app", "requirements.txt"), "w") as f:
            f.write(writer_requirements.print_django_style())

        self.models_content = data["models"]
        self.views_content = data["views"]
        self.writer_models = data["model_element"]
        writer_urls.set_classes(self.writer_models.get_classes())
        with open(os.path.join(os.getcwd(), "app", "urls.py"), "w") as f:
            f.write(writer_urls.print_django_style())

    def tearDown(self):
        # Cleanup the generated files and directories.
        zip_file = f"{self.project_name}.zip"
        project_dir = f"project_{self.project_name}"
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        for file in [
            zip_file,
            f"{self.project_name}_models.py",
            f"{self.project_name}_views.py",
            os.path.join("app", "requirements.txt"),
            os.path.join("app", "urls.py"),
        ]:
            if os.path.exists(file):
                os.remove(file)

    def test_generate_file_to_be_downloaded_invalid_project_name(self):
        """
        If an invalid project name is provided (e.g., contains whitespace or digits)
        then create_django_project should raise a ValueError. Since generate_file_to_be_downloaded
        calls create_django_project, this error will propagate.
        """
        invalid_project_name = "invalid project1"
        # Ensure that a zip file with invalid_project_name does not exist
        if os.path.exists(f"{invalid_project_name}.zip"):
            os.remove(f"{invalid_project_name}.zip")
        with self.assertRaises(ValueError) as context:
            generate_file_to_be_downloaded(
                invalid_project_name,
                self.models_content,
                self.views_content,
                self.writer_models,
            )
        self.assertIn(
            "Project name must not contain whitespace or number!",
            str(context.exception),
        )

    def test_zip_file_contents_include_all_required_files(self):
        """
        Verify that the zip file generated contains the required files.
        This list is compared against the expected list from the generation process.
        """
        generate_file_to_be_downloaded(
            self.project_name,
            self.models_content,
            self.views_content,
            self.writer_models,
        )
        expected_files = [
            "ini/asgi.py",
            "manage.py",
            "ini/settings.py",
            "ini/urls.py",
            "ini/wsgi.py",
            "main/admin.py",
            "main/apps.py",
            "main/models.py",
            "main/tests.py",
            "main/views.py",
            "main/migrations/__init__.py",
            "main/__init__.py",
            "requirements.txt",
            "main/urls.py",
            "run.sh",
            "run.bat",
            "main/templates/create_shape.html",
            "main/templates/create_circle.html",
            "main/templates/create_circles.html",
            "main/forms.py",
            "main/templates/shape_list.html",
            "main/templates/circle_list.html",
            "main/templates/circles_list.html",
            "main/templates/edit_shape.html",
            "main/templates/edit_circle.html",
            "main/templates/landing_page.html",
            "templates/base.html",
        ]

        with zipfile.ZipFile(f"{self.project_name}.zip", "r") as zipf:
            zip_contents = zipf.namelist()
        for file in expected_files:
            self.assertIn(file, zip_contents)

    def test_generate_file_to_be_downloaded_html_files(self):
        """
        Verify that the generated zip file contains all HTML files
        that has been generated for each model.

        These files should follow the naming convention
        main/templates/create_<model_name>.html
        main/templates/read_<model_name>.html
        main/templates/edit_<model_name>.html
        """
        generate_file_to_be_downloaded(
            self.project_name,
            self.models_content,
            self.views_content,
            self.writer_models,
        )

        expected_html_files = [
            "main/templates/create_shape.html",
            "main/templates/create_circle.html",
            "main/templates/create_circles.html",
            "main/templates/shape_list.html",
            "main/templates/circle_list.html",
            "main/templates/circles_list.html",
            "main/templates/edit_shape.html",
            "main/templates/edit_circle.html",
            "main/templates/landing_page.html",
        ]

        with zipfile.ZipFile(f"{self.project_name}.zip", "r") as zipf:
            zip_contents = zipf.namelist()
            zip_contents = [
                file for file in zip_contents if file.startswith("main/templates/")
            ]

        for file in expected_html_files:
            self.assertIn(file, zip_contents)

    def test_get_names_from_classes(self):
        create_pages = generate_html_create_pages_django(self.writer_models)
        result = get_names_from_classes(self.writer_models, create_pages)
        expected_class = [
            "Shape",
            "Circle",
            "Circles",
        ]
        expected_pages = [
            '{% extends \'base.html\' %}\n{% block content %}\n    <h1>Create Shape </h1>\n    <form method="POST">\n        {% csrf_token %}\n        {{ form.as_p }} \n        <button type="submit">Create Shape</button>\n    </form>\n{% endblock content %}',  # noqa: E501
            '{% extends \'base.html\' %}\n{% block content %}\n    <h1>Create Circle </h1>\n    <form method="POST">\n        {% csrf_token %}\n        {{ form.as_p }} \n        <button type="submit">Create Circle</button>\n    </form>\n{% endblock content %}',  # noqa: E501
            '{% extends \'base.html\' %}\n{% block content %}\n    <h1>Create Circles </h1>\n    <form method="POST">\n        {% csrf_token %}\n        {{ form.as_p }} \n        <button type="submit">Create Circles</button>\n    </form>\n{% endblock content %}',  # noqa: E501
        ]
        for name, page in result.items():
            self.assertIn(name, expected_class)
            self.assertIn(page, expected_pages)
