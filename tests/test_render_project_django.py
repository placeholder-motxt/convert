import os
import shutil
import unittest

from app.main import create_django_project
from app.utils import render_project_django_template


class TestGenerateDjangoProjectTemplate(unittest.TestCase):
    def setUp(self):
        self.project_name = "test_project"

    # generate django project
    def test_generate_django_project_positive(self):
        result = create_django_project(self.project_name)
        zipfile_path = f"{self.project_name}.zip"
        folder_path = f"project_{self.project_name}"
        try:
            self.assertTrue(os.path.exists(folder_path))
            self.assertTrue(os.path.exists(zipfile_path))
            for file in os.listdir(folder_path):
                self.assertIn(
                    file, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
                )
            self.assertEqual(
                result, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
            )
        finally:
            if os.path.exists(zipfile_path):
                os.remove(zipfile_path)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_generate_django_project_positive_with_whitespace(self):
        result = create_django_project("test project")
        zipfile_path = "test_project.zip"
        folder_path = "project_test_project"
        try:
            self.assertTrue(os.path.exists(folder_path))
            for file in os.listdir(folder_path):
                self.assertIn(
                    file, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
                )
            self.assertTrue(os.path.exists(zipfile_path))
            self.assertEqual(
                result, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
            )
        finally:
            if os.path.exists(zipfile_path):
                os.remove(zipfile_path)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    # render django project from template
    def test_render_project_django_template_positive(self):
        folder_path = "project_test_project"
        try:
            result = render_project_django_template(
                "app/templates/django_project", {"project_name": self.project_name}
            )
            self.assertTrue(os.path.exists(folder_path))
            for file in os.listdir(folder_path):
                self.assertIn(
                    file, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
                )
            self.assertEqual(
                result, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
            )
        finally:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_render_project_django_template_positive_with_whitespace(self):
        folder_path = "project_test_project"
        try:
            result = render_project_django_template(
                "app/templates/django_project", {"project_name": "test project"}
            )
            self.assertTrue(os.path.exists(folder_path))
            for file in os.listdir(folder_path):
                self.assertIn(
                    file, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
                )
            self.assertEqual(
                result, ["asgi.py", "manage.py", "settings.py", "urls.py", "wsgi.py"]
            )
        finally:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
