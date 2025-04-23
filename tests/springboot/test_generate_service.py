import os
import unittest

from pytest import fixture
from pytest_bdd import given, scenarios, then, when

from app.generate_service_springboot.generate_service_springboot import (
    generate_service_java,
)
from app.models.diagram import ClassObject
from app.models.methods import ClassMethodObject
from app.models.properties import ParameterObject, TypeObject

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Go from tests/ to project-root/
FEATURE_PATH = os.path.join(
    BASE_DIR, "..", "features", "springboot", "generate_service.feature"
)


class TestGenerateService(unittest.TestCase):
    def test_generate_service(self):
        self.maxDiff = None
        class_object = ClassObject()
        class_object.set_name("Cart")
        class_object.set_is_public(True)
        project_name = "burhanpedia"

        output = generate_service_java(project_name, class_object)

        with open(
            "tests/springboot/test_service_data.txt", "r", encoding="utf-8"
        ) as file:
            expected_output = file.read()

        self.assertEqual(output.strip(), expected_output.strip())


# Behavior Test
scenarios(FEATURE_PATH)


@fixture
def context():
    return {}


@given(
    "the project name and class object with no method is processed and ready as context"
)
def prepare_context(context):
    class_object = ClassObject()
    class_object.set_name("Cart")
    class_object.set_is_public(True)

    context["project_name"] = "burhanpedia"
    context["class_object"] = class_object


@when("the jinja process the context")
def render_template_output(context):
    context["output"] = generate_service_java(
        context["project_name"], context["class_object"]
    )


@then("the service file content is generated for CRUD")
def check_output(context):
    with open("tests/springboot/test_service_data.txt", "r", encoding="utf-8") as file:
        expected_output = file.read()

    assert context["output"].strip() == expected_output.strip()


@given(
    "the project name and class object with method is processed and ready as context"
)
def prepare_context(context):
    class_object = ClassObject()
    class_object.set_name("Cart")
    class_object.set_is_public(True)
    method_with_parameters = ClassMethodObject()
    method_with_parameters.set_name("method_params")
    param = ParameterObject()
    param.set_name("param1")
    param_type = TypeObject()
    param_type.set_name("int")
    param.set_type(param_type)
    method_with_parameters.add_parameter(param)
    class_object.add_method(method_with_parameters)

    method_with_parameters = ClassMethodObject()
    method_with_parameters.set_name("method_param2")
    method_with_parameters.set_modifier("public")
    param = ParameterObject()
    param.set_name("param2")
    param_type = TypeObject()
    param_type.set_name("str")
    param.set_type(param_type)
    method_with_parameters.add_parameter(param)
    class_object.add_method(method_with_parameters)

    method_with_parameters = ClassMethodObject()
    method_with_parameters.set_name("method_param3")
    method_with_parameters.set_modifier("private")
    param = ParameterObject()
    param.set_name("param3")
    param_type = TypeObject()
    param_type.set_name("boolean")
    param.set_type(param_type)
    method_with_parameters.add_parameter(param)
    class_object.add_method(method_with_parameters)

    context["project_name"] = "burhanpedia"
    context["class_object"] = class_object


@when("the jinja process the context")
def render_template_output(context):
    context["output"] = generate_service_java(
        context["project_name"], context["class_object"]
    )


@then("the service file content is generated for CRUD and method")
def check_output(context):
    with open(
        "tests/springboot/test_service_data_method.txt", "r", encoding="utf-8"
    ) as file:
        expected_output = file.read()

    assert (
        context["output"].replace(" ", "").replace("\n", "").strip()
        == expected_output.replace(" ", "").replace("\n", "").strip()
    )


@given(
    "the project name and private class object with method is processed and ready as context"
)
def prepare_context(context):
    class_object = ClassObject()
    class_object.set_name("Cart")
    class_object.set_is_public(False)
    method_with_parameters = ClassMethodObject()
    method_with_parameters.set_name("method_params")
    param = ParameterObject()
    param.set_name("param1")
    param_type = TypeObject()
    param_type.set_name("int")
    param.set_type(param_type)
    method_with_parameters.add_parameter(param)
    class_object.add_method(method_with_parameters)

    method_with_parameters = ClassMethodObject()
    method_with_parameters.set_name("method_param2")
    method_with_parameters.set_modifier("public")
    param = ParameterObject()
    param.set_name("param2")
    param_type = TypeObject()
    param_type.set_name("str")
    param.set_type(param_type)
    method_with_parameters.add_parameter(param)
    class_object.add_method(method_with_parameters)

    method_with_parameters = ClassMethodObject()
    method_with_parameters.set_name("method_param3")
    method_with_parameters.set_modifier("private")
    param = ParameterObject()
    param.set_name("param3")
    param_type = TypeObject()
    param_type.set_name("boolean")
    param.set_type(param_type)
    method_with_parameters.add_parameter(param)
    class_object.add_method(method_with_parameters)

    context["project_name"] = "burhanpedia"
    context["class_object"] = class_object


@when("the jinja process the context")
def render_template_output(context):
    context["output"] = generate_service_java(
        context["project_name"], context["class_object"]
    )


@then("the service file content is generated for methods only")
def check_output(context):
    with open(
        "tests/springboot/test_service_method_only.txt", "r", encoding="utf-8"
    ) as file:
        expected_output = file.read()
    assert (
        context["output"].replace(" ", "").replace("\n", "").strip()
        == expected_output.replace(" ", "").replace("\n", "").strip()
    )


@given("the project name and private class object with no method and ready as context")
def prepare_context(context):
    class_object = ClassObject()
    class_object.set_name("Cart")
    class_object.set_is_public(False)

    context["project_name"] = "burhanpedia"
    context["class_object"] = class_object


@when("the jinja process the context")
def render_template_output(context):
    context["output"] = generate_service_java(
        context["project_name"], context["class_object"]
    )


@then("the service file content is generated with empty method")
def check_output(context):
    expected_output = """package com.example.burhanpedia.service;

import com.example.burhanpedia.model.Cart;
import com.example.burhanpedia.repository.CartRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CartService {

    private final CartRepository cartRepository;


}
"""
    
    assert (
        context["output"].replace(" ", "").strip()
        == expected_output.replace(" ", "").strip()
    )
