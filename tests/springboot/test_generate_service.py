import unittest
import os
from pytest_bdd import scenarios, given, when, then
from pytest import fixture
from app.generate_service_springboot.generate_service_springboot import generate_service_java
from app.models.diagram import ClassObject

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Go from tests/ to project-root/
FEATURE_PATH = os.path.join(BASE_DIR, "..", "features", "springboot", "generate_service.feature")

class TestGenerateService(unittest.TestCase):
    def test_generate_service(self):
        class_object = ClassObject()
        class_object.set_name("Cart")
        project_name = "burhanpedia"

        output = generate_service_java(project_name, class_object)

        with open("tests/springboot/test_service_data.txt", "r", encoding="utf-8") as file:
            expected_output = file.read()
        
        self.assertEqual(output.strip(), expected_output.strip())

# Behavior Test
scenarios(FEATURE_PATH)

@fixture
def context():
    return {}

@given("the project name and class object is processed and ready as context")
def prepare_context(context):
    class_object = ClassObject()
    class_object.set_name("Cart")

    context["project_name"] = "burhanpedia"
    context["class_object"] = class_object

@when("the jinja process the context")
def render_template_output(context):
    context["output"] = generate_service_java(context["project_name"], context["class_object"])

@then("the service file content is generated")
def check_output(context):
    with open("tests/springboot/test_service_data.txt", "r", encoding="utf-8") as file:
        expected_output = file.read()
    
    assert context["output"].strip() == expected_output.strip()
