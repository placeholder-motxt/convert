import json
import os
import shutil
import unittest
import zipfile

from app.main import create_django_app, create_django_project, render_model


class TestReplaceModel(unittest.TestCase):
    def remove_used_project(self):
        if os.path.exists("testRenderModel.zip"):
            os.remove("testRenderModel.zip")
        if os.path.exists("project_testRenderModel"):
            shutil.rmtree("project_testRenderModel")

    def setUp(self):
        self.remove_used_project()

    def test_render_model(self):
        with open("tests/test_input.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        output = render_model(json.loads(json_data))
        self.assertEqual(output.strip(), expected_result.strip())

    def test_render_model_in_zip(self):
        with open("tests/test_input.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        output = render_model(json.loads(json_data))
        create_django_project("testRenderModel")
        create_django_app("testRenderModel", "testRender", output)
        with zipfile.ZipFile("testRenderModel.zip", "r") as zipf:
            self.assertIn(
                "testRender/models.py",
                zipf.namelist(),
                "models.py should exist in the zip file",
            )

            models_content = zipf.read("testRender/models.py").decode("utf-8")
            self.assertEqual(models_content, expected_result)

    def test_empty_model_in_zip(self):
        with open("tests/test_default_models.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        output = ""
        create_django_project("testRenderModel")
        create_django_app("testRenderModel", "testRender", output)
        with zipfile.ZipFile("testRenderModel.zip", "r") as zipf:
            self.assertIn(
                "testRender/models.py",
                zipf.namelist(),
                "models.py should exist in the zip file",
            )

            models_content = zipf.read("testRender/models.py").decode("utf-8")
            self.assertEqual(models_content, expected_result)

    def tearDown(self):
        self.remove_used_project()
