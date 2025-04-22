import unittest

from app.generate_runner.generate_runner import (
    generate_springboot_linux_runner,
    generate_springboot_window_runner,
)


class TestModelsElements(unittest.TestCase):
    def test_generate_springboot_runner(self):
        expected = r".\gradlew.bat bootRun"
        self.assertEqual(expected, generate_springboot_window_runner())

    def test_generate_springboot_linux_runner(self):
        expected = "#!/bin/bash\n\n./gradlew bootRun"
        self.assertEqual(expected, generate_springboot_linux_runner())
