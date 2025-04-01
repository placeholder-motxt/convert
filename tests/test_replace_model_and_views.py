import os
import shutil
import unittest
import zipfile

import pytest
from fastapi import HTTPException

from app.main import (
    create_django_app,
    create_django_project,
    fetch_data,
    render_model,
    render_views,
)


class TestReplaceModelAndViews(unittest.TestCase):
    maxDiff = None

    def remove_used_project(self):
        if os.path.exists("testRenderModel.zip"):
            os.remove("testRenderModel.zip")
        if os.path.exists("project_testRenderModel"):
            shutil.rmtree("project_testRenderModel")

    def setUp(self):
        self.remove_used_project()

    def test_render_model(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result_model.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        output = render_model(processed_data)

        self.assertEqual(output.strip().replace("\t", "    "), expected_result.strip())

    def test_render_model_in_zip(self):
        with open("tests/test_render_model.txt", "r", encoding="utf-8") as file:
            json_data = file.read()

        with open("tests/test_result_model.txt", "r", encoding="utf-8") as file:
            expected_result = file.read()

        processed_data = fetch_data(["tes.class.jet"], [[json_data]])

        output = render_model(processed_data)

        create_django_project("testRenderModel")
        create_django_app("testRenderModel", "testRender", output)
        with zipfile.ZipFile("testRenderModel.zip", "r") as zipf:
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
        with pytest.raises(HTTPException) as excinfo:
            fetch_data(["tes.class.jet"], [["{diagram: 'ClassDiagram'}"]])

        assert excinfo.value.status_code == 422

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

        output = render_views(processed_data)

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

        output_models = render_model(processed_data)
        output_views = render_views(processed_data)

        create_django_project("testRenderModel")
        create_django_app("testRenderModel", "testRender", output_models, output_views)
        with zipfile.ZipFile("testRenderModel.zip", "r") as zipf:
            self.assertIn(
                "testRender/views.py",
                zipf.namelist(),
                "views.py should exist in the zip file",
            )

            models_content = zipf.read("testRender/views.py").decode("utf-8")
            self.assertEqual(
                models_content.strip().replace("\t", "    "), expected_result.strip()
            )

    def tearDown(self):
        self.remove_used_project()
