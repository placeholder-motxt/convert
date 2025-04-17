import os
import unittest

from app.generate_swagger.generate_swagger import generate_swagger_config

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestGenerateSwagger(unittest.TestCase):
    def test_generate_swagger_config(self):
        with open(os.path.join(TEST_DIR, "test_swagger_config.txt")) as f:
            expected = f.read().strip()

            res = generate_swagger_config("project")

            self.assertEqual(res, expected)
