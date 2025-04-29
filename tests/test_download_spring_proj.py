import tempfile
import unittest
import zipfile
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.utils import is_valid_java_package_name

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
            f.writestr("src", "")
            f.writestr("src/main", "")
            f.writestr("src/main/java", "")
            f.writestr("src/main/java/com", "")
            f.writestr("src/main/java/com/motxt", "")
            f.writestr("src/main/java/com/motxt/spring", "")
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
            f.writestr("src", "")
            f.writestr("src/main", "")
            f.writestr("src/main/java", "")
            f.writestr("src/main/java/com", "")
            f.writestr("src/main/java/com/example", "")
            f.writestr("src/main/java/com/example/spring", "")
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
        for group_id in ["123.abcd", ":a.ha", ".abcd", "hjk.", "int.abc"]:
            self.json["group_id"] = group_id
            package_name = f"{self.json['project_name']}.{group_id}"
            resp = client.post("/convert", json=self.json)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json()["detail"], f"Invalid Java package name: {package_name}"
            )

    async def test_invalid_project_name_valid_group_id(self):
        """
        When project_name is invalid but group id is valid it should
        still return an error
        """
        self.json["group_id"] = "spring.example"
        for project_name in ["123", ".bakfsd", ":fsf", "abscd.", "class.abc"]:
            self.json["project_name"] = project_name
            package_name = f"{project_name}.{self.json['group_id']}"
            resp = client.post("/convert", json=self.json)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(
                resp.json()["detail"], f"Invalid Java package name: {package_name}"
            )

    async def test_valid_group_id(self):
        for group_id in ["com.example", "abc.def", "A_asdf.K_", "_asf123._32"]:
            self.assertTrue(is_valid_java_package_name(group_id))
