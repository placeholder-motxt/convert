import os
import unittest

from app.generate_repository.generate_repository import generate_repository_java
from app.models.diagram import ClassObject

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


# Tests for generate_html_read_page_django
class TestGenerateRepository(unittest.TestCase):
    def test_generate_repository_java(self):
        with open(os.path.join(TEST_DIR, "test_repository.txt")) as f:
            expected = f.read().strip()
            kelas = ClassObject()
            kelas.set_name("kelas")
            self.assertEqual(expected, generate_repository_java("projek", kelas))
