import tempfile
import unittest
import zipfile
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestDownloadSpringProject(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.json = {
            "filename": ["test_spring"],
            "content": [["test content"]],
            "project_name": "spring",
            "group_id": "com.motxt",
            "project_type": "spring",
        }

    @patch("app.main.convert_spring")
    async def test_correct_proj_type(self, mock_spring: AsyncMock):
        """Should be modified after PBI 8-3 gets merged"""
        tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        with zipfile.ZipFile(tmp_zip.name, "w") as f:
            f.writestr("build.gradle.kts", "testing")
            f.mkdir("src")
            f.mkdir("src/main")
            f.mkdir("src/main/java")
            f.mkdir("src/main/java/com")
            f.mkdir("src/main/java/com/motxt")
            f.mkdir("src/main/java/com/motxt/spring")
        tmp_zip.close()
        mock_spring.return_value = tmp_zip.name
        resp = client.post("/convert", json=self.json)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/zip")
        self.assertIn(b"PK\x03\x04", resp.content)
        self.assertIn(b"build.gradle.kts", resp.content)
        self.assertIn(b"motxt", resp.content)

    @patch("app.main.convert_spring")
    async def test_empty_group_id(self, mock_spring: AsyncMock):
        """
        When group_id is empty, will use com.example
        Should be modified after PBI 8-3 gets merged
        """
        tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        with zipfile.ZipFile(tmp_zip.name, "w") as f:
            f.mkdir("src")
            f.mkdir("src/main")
            f.mkdir("src/main/java")
            f.mkdir("src/main/java/com")
            f.mkdir("src/main/java/com/example")
            f.mkdir("src/main/java/com/example/spring")
        tmp_zip.close()
        mock_spring.return_value = tmp_zip.name
        self.json.pop("group_id")
        resp = client.post("/convert", json=self.json)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"com", resp.content)
        self.assertIn(b"example", resp.content)

    async def test_invalid_group_id(self):
        """
        When group_id is not following java package naming conventions
        it should return 400 and a message telling it is an invalid group_id
        """
        for group_id in ["123.abcd", ":a.ha", ".abcd", "hjk.", "ab;cd;ef"]:
            self.json["group_id"] = group_id
            resp = client.post("/convert", json=self.json)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json()["detail"], f"Invalid group id: {group_id}")
