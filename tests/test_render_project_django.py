import os
import shutil
import unittest
import zipfile

from app.main import create_django_project
from app.utils import render_project_django_template


class TestGenerateDjangoProjectTemplate(unittest.TestCase):
    def setUp(self):
        self.project_name = "test_project"
        if os.path.exists(f"{self.project_name}.zip"):
            os.remove(f"{self.project_name}.zip")
        if os.path.exists(f"project_{self.project_name}"):
            shutil.rmtree(f"project_{self.project_name}")

    # generate django project
    def test_generate_django_project_positive(self):
        result = create_django_project(self.project_name)
        zipfile_path = f"{self.project_name}.zip"
        folder_path = f"project_{self.project_name}"
        try:
            self.assertTrue(os.path.exists(folder_path))
            self.assertTrue(os.path.exists(zipfile_path))
            for file in os.listdir(folder_path):
                self.assertIn(file, result)
                print(file)
                with (
                    open(os.path.join(folder_path, file), "r") as f1,
                    open(f"tests\\testdata\\{file}.txt", "r") as f2,
                ):
                    self.assertEqual(f1.read(), f2.read())
        finally:
            if os.path.exists(zipfile_path):
                os.remove(zipfile_path)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_generate_django_project_negative_with_whitespace(self):
        with self.assertRaises(ValueError) as context:
            create_django_project("test project")
        self.assertEqual(
            str(context.exception),
            "Project name must not contain whitespace or number!",
        )
        if os.path.exists("project_test_project"):
            shutil.rmtree("project_test_project")
        if os.path.exists("test_project.zip"):
            os.remove("test_project.zip")

    def test_generate_django_project_negative_with_existing_zipfile(self):
        zipfile_path = f"{self.project_name}.zip"
        with zipfile.ZipFile(zipfile_path, "w") as zipf:
            zipf.writestr(self.project_name, data="")  # create empty file
        try:
            with self.assertRaises(ValueError) as context:
                create_django_project(self.project_name)
            self.assertEqual(
                str(context.exception),
                f"File {self.project_name}.zip already exists",
            )
        finally:
            if os.path.exists(zipfile_path):
                os.remove(zipfile_path)
        if os.path.exists("project_test_project"):
            shutil.rmtree("project_test_project")

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
