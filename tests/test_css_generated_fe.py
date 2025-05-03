import os
import tempfile
import unittest
import zipfile

import anyio
from fastapi.testclient import TestClient

from app.main import app, convert_django

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")
CSS_DIR = os.path.join(CUR_DIR, "..", "app", "templates", "css")


class TestCssGeneratedFrontend(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        with open(os.path.join(TEST_DIR, "BurhanpediaLite.class.jet")) as f:
            self.class_diag = f.read()

        self.filenames = ["BurhanpediaLite.class.jet"]
        self.contents = [[self.class_diag]]
        self.project_name = "test_css"
        self.payload = {
            "filename": ["BurhanpediaLite.class.jet"],
            "content": [[self.class_diag]],
            "project_name": "test_css",
        }
        self.client = TestClient(app)

    def test_no_style_in_request_return_default_style(self):
        resp = self.client.post("/convert", json=self.payload)
        self.assertEqual(resp.status_code, 200)

        with open(os.path.join(CSS_DIR, "modern.css")) as f:
            expected_css = f.read()
        with tempfile.TemporaryFile() as f:
            f.write(resp.content)
            f.seek(0)
            with zipfile.ZipFile(f, "r") as zipf:
                self.assertIn("static/css/style.css", zipf.namelist())
                with zipf.open("static/css/style.css") as cssf:
                    self.assertEqual(expected_css, cssf.read().decode("utf-8"))

    def test_no_error_all_known_styles(self):
        """Positive case style sent is known value"""
        styles = ["classic", "dark", "minimalist", "modern", "vibrant"]
        for style in styles:
            self.payload["style_theme"] = style
            resp = self.client.post("/convert", json=self.payload)
            self.assertEqual(resp.status_code, 200)

    def test_unknown_style_value(self):
        """
        Negative case style sent is not a know value.
        Should be catched by Pydantic hence the 422 resp code
        """
        styles = ["abcd", "idk123", "style.css"]
        for style in styles:
            self.payload["style_theme"] = style
            resp = self.client.post("/convert", json=self.payload)
            self.assertEqual(resp.status_code, 422)

    async def test_all_styles_give_correct_result(self):
        self.maxDiff = None
        styles = ["classic", "dark", "minimalist", "modern", "vibrant"]
        for style in styles:
            async with await anyio.open_file(
                os.path.join(CSS_DIR, f"{style}.css")
            ) as f:
                expected = await f.read()
            tmp_zip_path = await convert_django(
                self.project_name, self.filenames, self.contents, style
            )
            with zipfile.ZipFile(tmp_zip_path, "r") as zipf:
                with zipf.open("static/css/style.css") as f:
                    self.assertEqual(expected, f.read().decode("utf-8"))

            os.remove(tmp_zip_path)

    async def test_static_related_settings_are_added(self):
        tmp_zip_path = await convert_django(
            self.project_name, self.filenames, self.contents, "modern"
        )
        with zipfile.ZipFile(tmp_zip_path, "r") as zipf:
            with zipf.open("templates/base.html") as basef:
                self.assertIn(
                    """<link rel="stylesheet" href="{% static 'css/style.css' %}">""",
                    basef.read().decode("utf-8"),
                )

            with zipf.open(f"{self.project_name}/settings.py") as settingsf:
                self.assertIn(
                    "STATICFILES_DIRS = [BASE_DIR / 'static']",
                    settingsf.read().decode("utf-8"),
                )
        os.remove(tmp_zip_path)
