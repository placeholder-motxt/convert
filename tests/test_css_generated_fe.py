import os
import tempfile
import unittest
import zipfile

from fastapi.testclient import TestClient

from app.main import app

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")
CSS_DIR = os.path.join(CUR_DIR, "..", "app", "templates", "css")


class TestCssGeneratedFrontend(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(TEST_DIR, "BurhanpediaLite.class.jet")) as f:
            self.class_diag = f.read()

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
                filenames = zipf.namelist()
                self.assertIn("css/", filenames)
                self.assertIn("css/style.css", filenames)
                with zipf.open("css/style.css") as cssf:
                    self.assertEqual(expected_css, cssf.read())

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
