import os
import unittest

from app.generate_sqlite_config.generate_sqlite_config import generate_sqlitedialect

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestRenderRunScript(unittest.TestCase):
    def test_generate_sqlite_config(self):
        with open(os.path.join(TEST_DIR, "test_SQLiteDialect.txt")) as file:
            expected = file.read().strip()

        rendered = generate_sqlitedialect("projek", "com.example")
        self.assertEqual(rendered.strip(), expected)
