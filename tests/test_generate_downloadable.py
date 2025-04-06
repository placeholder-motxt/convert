import json
import os
import shutil
import unittest
import zipfile

from app.main import (
    fetch_data,
    generate_file_to_be_downloaded,
)
from app.models.elements import RequirementsElements, UrlsElement


class TestGenerateFileToBeDownloaded(unittest.TestCase):
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
            "main/__init__.py",
            "requirements.txt",
            "main/urls.py",
            "run.sh",
            "run.bat",
            "main/templates/create_buku.html",
            "main/templates/create_peminjaman.html",
            "main/templates/create_copybuku.html",
            "main/forms.py",
            "main/templates/read_buku.html",
            "main/templates/read_peminjaman.html",
            "main/templates/read_copybuku.html",
            "main/templates/edit_buku.html",
            "main/templates/edit_peminjaman.html",
            "main/templates/edit_copybuku.html",
            "main/templates/landing_page.html",
            "templates/base.html",
        ]
        for path in result:
            self.assertIn(path, expected_output)
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
