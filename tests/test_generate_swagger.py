import os
import unittest

from app.generate_swagger.generate_swagger import (
    generate_swagger_config,
    get_swagger_controller_import,
    get_swagger_decorators,
)
from app.models.diagram import ClassObject

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestGenerateSwagger(unittest.TestCase):
    def test_generate_swagger_config(self):
        with open(os.path.join(TEST_DIR, "test_swagger_config.txt")) as f:
            expected = f.read().strip()
            res = generate_swagger_config("project")
            self.assertEqual(res, expected)

    def test_get_swagger_controller_import(self):
        self.assertEqual(
            "import io.swagger.v3.oas.annotations.Operation;\n",
            get_swagger_controller_import(),
        )

    def test_get_swagger_decorators(self):
        kelas = ClassObject()
        kelas.set_name("kelas")
        self.assertEqual(
            {
                "create_swagger": '@Operation(summary = "Create a new kelas")',
                "read_swagger": '@Operation(summary = "Get a kelas by ID")',
                "update_swagger": '@Operation(summary = "Update an existing kelas")',
                "delete_swagger": '@Operation(summary = "Delete a kelas by ID")',
            },
            get_swagger_decorators(kelas),
        )
