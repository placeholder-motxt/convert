import os
import subprocess
import tempfile
import time
import unittest
import zipfile

import anyio
import requests
from fastapi.testclient import TestClient

from app.config import SPRING_SERVICE_URL
from app.main import app, initialize_springboot_zip

client = TestClient(app)
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
test_diag = os.path.join(CUR_DIR, "..", "testdata", "BurhanpediaLite.class.jet")
with open(test_diag) as f:
    test_diag_content = f.read()


class TestIntegrationInitializeSpring(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cmd = [
            "docker",
            "run",
            "--rm",
            "--name",
            "spring",
            "-p",
            "8080:8080",
            "-e",
            "HTTP_PROXY_PORT=9999",
            "-d",
            "mightyzanark/spring-initializr:1.0.2",
        ]
        subprocess.run(cmd)

        max_attempts = 10
        for _ in range(max_attempts):
            try:
                resp = requests.get(SPRING_SERVICE_URL, timeout=1)
                if resp.status_code == 200:
                    return
            except (requests.RequestException, requests.ConnectionError):
                time.sleep(1)

        exit("Unable to start initializr")

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["docker", "stop", "spring"])

    def setUp(self):
        self.json = {
            "filename": ["test_spring"],
            "content": [[test_diag_content]],
            "project_name": "spring",
            "group_id": "com.motxt",
            "project_type": "spring",
        }

    async def test_openapi_spring_mvc_in_build_gradle_has_version(self):
        tmp_zip_path = await initialize_springboot_zip("any", "com.motxt")
        with zipfile.ZipFile(tmp_zip_path) as zipf:
            with zipf.open("build.gradle.kts") as buildf:
                self.assertIn(
                    "org.springdoc:springdoc-openapi-starter-webmvc-ui:2.2.0",
                    buildf.read().decode("utf-8"),
                )

    async def test_application_properties_properly_filled(self):
        expected = ""
        async with await anyio.open_file(
            os.path.join(CUR_DIR, "expected_app_properties.txt")
        ) as f:
            expected = await f.read()

        tmp_zip_path = await initialize_springboot_zip("testapp", "com.motxt")
        with zipfile.ZipFile(tmp_zip_path) as zipf:
            with zipf.open("src/main/resources/application.properties") as f:
                self.assertEqual(expected, f.read().decode("utf-8"))

    async def test_no_duplicate_files(self):
        resp = client.post("/convert", json=self.json)
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(resp.content)
            temp.seek(0)
            with zipfile.ZipFile(temp) as zipf:
                namelist = zipf.namelist()
                unique_names = set(namelist)
                self.assertCountEqual(namelist, unique_names)
