import unittest

from app.models.elements import RunBashScriptElements, RunBatScriptElements


class TestRenderRunScript(unittest.TestCase):
    def setUp(self):
        self.bash_script_element = RunBashScriptElements("run.sh")
        self.bat_script_element = RunBatScriptElements("run.bat")

    def test_bash_print_django_style(self):
        with open("tests/test_run_sh.txt", "r", encoding="utf-8") as file:
            sh = file.read()

        rendered = self.bash_script_element.print_django_style()
        self.assertEqual(rendered.strip(), sh.strip())

    def test_bat_print_django_style(self):
        with open("tests/test_run_bat.txt", "r", encoding="utf-8") as file:
            bat = file.read()

        rendered = self.bat_script_element.print_django_style()
        self.assertEqual(rendered.strip(), bat.strip())
