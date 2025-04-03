import json
import os
import shutil
import unittest
import zipfile

from app.main import (
    fetch_data,
    generate_file_to_be_downloaded,
)


class TestGenerateFileToBeDownloaded(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and switch to it.
        with open("tests/testdata/input_generate_file_to_be_downloaded.json", "r") as f:
            json_data = json.load(f)
        self.filename = json_data["filename"]
        self.content = json_data["content"]
        data = fetch_data(self.filename, self.content)
        self.models_content = data["models_content"]
        self.views_content = data["views_content"]
        self.writer_models = data["writer_models"]
        self.writer_views = data["writer_views"]
        self.project_name = self.filename.split[0]

    def tearDown(self):
        if os.path.exists("requirements.txt"):
            os.remove("requirements.txt")
        if os.path.exists("urls.py"):
            os.remove("urls.py")
        # Remove any created zip file or project folder.
        if os.path.exists("file1.zip"):
            os.remove("file1.zip")
        if os.path.exists("project_file1"):
            shutil.rmtree("project_file1")

        if os.path.exists(f"project_{self.project_name}"):
            shutil.rmtree(f"project_{self.project_name}")
        if os.path.exists(f"{self.project_name}_models.py"):
            os.remove(f"{self.project_name}_models.py")
        if os.path.exists(f"{self.project_name}_views.py"):
            os.remove(f"{self.project_name}_views.py")
        if os.path.exists("requirements.txt"):
            os.remove("requirements.txt")
        if os.path.exists("urls.py"):
            os.remove("urls.py")

    def test_generate_file_to_be_downloaded(self):
        # Act: Call the function to generate the downloadable file.
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
            "main/templates/create_Buku_page_django.html",
            "main/templates/create_Peminjaman_page_django.html",
            "main/templates/create_CopyBuku_page_django.html",
            "main/forms.py",
            "main/templates/read_Buku_page_django.html",
            "main/templates/read_Peminjaman_page_django.html",
            "main/templates/read_CopyBuku_page_django.html",
            "main/templates/edit_Buku_page_django.html",
            "main/templates/edit_Peminjaman_page_django.html",
            "main/templates/edit_CopyBuku_page_django.html",
            "main/templates/landing_page.html",
            "templates/base.html",
        ]
        with zipfile.ZipFile(f"{self.project_name}.zip", "r") as zipf:
            for file in zipf.namelist():
                self.assertIn(file, expected_output)
                self.assertIn(result, expected_output)
