import os
import shutil
import tempfile
import unittest
import zipfile
from unittest.mock import patch

from app.main import create_django_app, create_django_project
from app.utils import get_random_secret_key, render_project_django_template


class TestGenerateDjangoProjectTemplate(unittest.TestCase):
    def setUp(self):
        self.project_name = "test_project"
        if os.path.exists(f"{self.project_name}.zip"):
            os.remove(f"{self.project_name}.zip")
        if os.path.exists(f"project_{self.project_name}"):
            shutil.rmtree(f"project_{self.project_name}")

        self.tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)

    def tearDown(self):
        self.tmp_zip.close()
        os.remove(self.tmp_zip.name)

    # generate django project
    def test_generate_django_project_positive(self):
        mocked_secret_key = get_random_secret_key()
        with open("tests/testdata/settings.py.txt", "r") as file_to_read:
            settings = file_to_read.read()
        settings_mock = settings.replace(
            "SECRET_KEY = ''", f"SECRET_KEY = '{mocked_secret_key}'"
        )
        with open("tests/testdata/settings.py.txt", "w") as file_to_edit:
            file_to_edit.write(settings_mock)

        # Mock get_random_secret_key to return a predictable value
        with patch("app.utils.get_random_secret_key", return_value=mocked_secret_key):
            result = create_django_project(self.project_name, self.tmp_zip.name)
            zipfile_path = self.tmp_zip.name
            folder_path = f"project_{self.project_name}"
            try:
                self.assertTrue(os.path.exists(folder_path))
                self.assertTrue(os.path.exists(zipfile_path))
                for file in os.listdir(folder_path):
                    self.assertIn(file, result)
                    with (
                        open(os.path.join(folder_path, file), "r") as f1,
                        open(
                            os.path.join("tests", "testdata", f"{file}.txt"), "r"
                        ) as f2,
                    ):
                        self.assertEqual(f1.read(), f2.read())
            finally:
                with open(
                    "tests/testdata/settings.py.txt", "w", newline="\n"
                ) as file_to_edit:
                    file_to_edit.write(settings)
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)

    def test_generate_django_project_negative_with_whitespace(self):
        with self.assertRaises(ValueError) as context:
            create_django_project("test project", self.tmp_zip.name)
        self.assertEqual(
            str(context.exception),
            "Project name must not contain whitespace or number!",
        )
        if os.path.exists("project_test_project"):
            shutil.rmtree("project_test_project")
        if os.path.exists("test_project.zip"):
            os.remove("test_project.zip")

    # render django project from template
    def test_render_project_django_template_positive(self):
        folder_path = "project_test_project"
        try:
            result = render_project_django_template(
                "app/templates/django_project", {"project_name": self.project_name}
            )
            self.assertTrue(os.path.exists(folder_path))
            for file in os.listdir(folder_path):
                self.assertIn(file, result)
        finally:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_render_project_django_template_negative_with_whitespace(self):
        with self.assertRaises(ValueError) as context:
            render_project_django_template(
                "app/templates/django_project", {"project_name": "test project"}
            )
        self.assertEqual(
            str(context.exception),
            "Project name must not contain whitespace or number!",
        )
        if os.path.exists("project_test_project"):
            shutil.rmtree("project_test_project")

    def test_render_project_django_template_negative_with_existing_folder(self):
        folder_path = "project_test_project"
        os.makedirs(folder_path, exist_ok=True)
        try:
            with self.assertRaises(FileExistsError) as context:
                render_project_django_template(
                    "app/templates/django_project", {"project_name": self.project_name}
                )
            self.assertEqual(
                str(context.exception),
                "Folder project_test_project already exists",
            )
        finally:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)


class TestGenerateDjangoMain(unittest.TestCase):
    def setUp(self):
        self.project_name = "test_main"
        if os.path.exists(f"{self.project_name}.zip"):
            os.remove(f"{self.project_name}.zip")
        if os.path.exists(f"project_{self.project_name}"):
            shutil.rmtree(f"project_{self.project_name}")

        self.tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)

    def tearDown(self):
        self.tmp_zip.close()
        os.remove(self.tmp_zip.name)

    def test_generate_django_app_positive(self):
        folder_path = "project_test_main"
        create_django_project("test_main", self.tmp_zip.name)
        create_django_app("test_main", "main", self.tmp_zip.name)

        zipfile_path = self.tmp_zip.name
        open_zip = zipfile.ZipFile(zipfile_path, "r")
        files = open_zip.namelist()

        for file in files:
            filename = file.split("/")[-1]
            django_app = os.listdir("app/templates/django_app")
            django_app.remove("apps.py.j2")
            if filename.replace(".py", ".txt") in django_app:
                if "migrations" in file:
                    continue
                with (
                    open_zip.open(file, "r") as f1,
                    open(
                        os.path.join(
                            "app",
                            "templates",
                            "django_app",
                            f"{filename.replace('.py', '.txt')}",
                        ),
                        "r",
                    ) as f2,
                ):
                    self.assertEqual(
                        f1.read().decode("utf-8").strip(), f2.read().strip()
                    )
            elif filename == "apps.py":
                with (
                    open_zip.open(file) as f1,
                    open(os.path.join("tests", "testdata", "apps.py.txt"), "r") as f2,
                ):
                    self.assertEqual(
                        f1.read().decode("utf-8").strip(), f2.read().strip()
                    )
        open_zip.close()
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    def test_generate_django_app_negative_invalid_name(self):
        with self.assertRaises(ValueError) as context:
            create_django_app("test_main", "buku pin", self.tmp_zip.name)
        self.assertEqual(
            str(context.exception),
            "App name must not contain whitespace!",
        )

    def test_generate_django_app_negative_invalid_project_name(self):
        with self.assertRaises(ValueError) as context:
            create_django_app("test main", "main", self.tmp_zip.name)
        self.assertEqual(
            str(context.exception),
            "Project name must not contain whitespace!",
        )

    def test_generate_django_app_negative_zip_not_exist(self):
        with self.assertRaises(FileNotFoundError) as context:
            create_django_app("test_main", "main", "test_main.zip")
        self.assertEqual(
            str(context.exception),
            "File test_main.zip does not exist",
        )
