import os
import shutil
import tempfile
import unittest
import zipfile

import pytest

from app.main import (
    create_django_app,
    create_django_project,
    fetch_data,
)
from app.models.elements import ModelsElements


class TestReplaceModelAndViews(unittest.TestCase):
    maxDiff = None

    def remove_used_project(self):
        if os.path.exists(self.tmp_zip.name):
            os.remove(self.tmp_zip.name)
        if os.path.exists("project_testRenderModel"):
            shutil.rmtree("project_testRenderModel")

    def setUp(self):
        self.tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)

    def tearDown(self):
        self.tmp_zip.close()
        self.remove_used_project()

    def test_render_model(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result_model.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        output = processed_data["models"]
        self.assertEqual(output.strip().replace("\t", "    "), expected_result.strip())

    def test_render_model_sort(self):
        with open("tests/test_render_model_sort.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result_model_sort.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        output = processed_data["models"]

        self.assertEqual(output.strip().replace("\t", "    ").replace(" ", ""), expected_result.replace(" ", "").strip())
    
    def test_render_complex_sort(self):
        with open("tests/test_render_complex_topo.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result_complex_topo.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        output = processed_data["models"]

        self.assertEqual(output.strip().replace("\t", "    ").replace(" ", ""), expected_result.replace(" ", "").strip())
    
    def test_render_cyclic_inheritance(self):
        with open("tests/test_cylic.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with self.assertRaises(ValueError) as ctx:
            fetch_data(["tes.class.jet"], [[json_data]])
        
        self.assertEqual(
            str(ctx.exception),
            "Cyclic Inheritance Detected at Test1",
        )

    def test_render_model_in_zip(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result_model.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        output = processed_data["models"]

        create_django_project("testRenderModel", self.tmp_zip.name)
        create_django_app("testRenderModel", "testRender", self.tmp_zip.name, output)
        with zipfile.ZipFile(self.tmp_zip.name, "r") as zipf:
            self.assertIn(
                "testRender/models.py",
                zipf.namelist(),
                "models.py should exist in the zip file",
            )

            models_content = zipf.read("testRender/models.py").decode("utf-8")
            self.assertEqual(
                models_content.strip().replace("\t", "    "), expected_result.strip()
            )

    def test_render_empty_model(self):
        with pytest.raises(ValueError) as excinfo:
            fetch_data(["tes.class.jet"], [['{"diagram": "ClassDiagram"}']])

        self.assertEqual(
            "Nodes not found in the json, \nplease make sure the file isn't corrupt".strip(),
            str(excinfo.value).strip(),
        )

    def test_render_views(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            model = file.read()

        with open("tests/test_render_views.txt", "r", encoding="utf-8") as file:
            views = file.read()

        with open("tests/test_result_views.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(
            ["tes.class.jet", "tes.sequence.jet"], [[model], [views]]
        )

        output = processed_data["views"]

        self.assertEqual(output.strip().replace("\t", "    "), expected_result.strip())

    def test_render_views_in_zip(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            model = file.read()

        with open("tests/test_render_views.txt", "r", encoding="utf-8") as file:
            views = file.read()

        with open("tests/test_result_views.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(
            ["tes.class.jet", "tes.sequence.jet"], [[model], [views]]
        )

        output_models = processed_data["models"]
        output_views = processed_data["views"]

        create_django_project("testRenderModel", self.tmp_zip.name)
        create_django_app(
            "testRenderModel",
            "testRender",
            self.tmp_zip.name,
            output_models,
            output_views,
        )
        with zipfile.ZipFile(self.tmp_zip.name, "r") as zipf:
            self.assertIn(
                "testRender/views.py",
                zipf.namelist(),
                "views.py should exist in the zip file",
            )

            models_content = zipf.read("testRender/views.py").decode("utf-8")
            self.assertEqual(
                models_content.strip().replace("\t", "    "), expected_result.strip()
            )

    def test_get_model_element(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        models = processed_data["model_element"]

        self.assertIsInstance(models, ModelsElements)
