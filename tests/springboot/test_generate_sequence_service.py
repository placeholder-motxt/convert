import unittest

import pytest

from app.generate_service_springboot.generate_service_springboot import (
    generate_sequence_service_java,
)
from app.models.elements import ViewsElements
from app.models.methods import (
    ArgumentObject,
    ClassMethodCallObject,
    ClassMethodObject,
    ControllerMethodCallObject,
    ControllerMethodObject,
)
from app.models.properties import ParameterObject, TypeObject


class TestGenerateSequenceService(unittest.TestCase):
    maxDiff = None

    def test_sequence_with_all_features(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")
        self.controller_method_1.set_return_type(str_type)

        self.parameter_1 = ParameterObject()
        self.parameter_1.set_name("parameter_1")
        self.parameter_1.set_type(str_type)

        self.controller_method_1.add_parameter(self.parameter_1)

        self.controller_method_call_1 = ControllerMethodCallObject()
        self.controller_method_call_1.set_method(self.controller_method_1)
        self.controller_method_call_1.set_condition("condition == True")
        self.controller_method_call_1.set_ret_var("ret_var_1")
        self.controller_method_call_1.set_return_var_type(str_type)

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.controller_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.controller_method_call_1.add_argument(self.argument_1)

        self.controller_method_1.add_call(self.controller_method_call_1)

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_return_var_type(str_type)
        self.class_method_call_1.set_instance_name("instance_1")

        self.controller_method_1.add_call(self.class_method_call_1)

        self.views_elements = ViewsElements("SequenceService.java")
        self.views_elements.add_controller_method(self.controller_method_1)

        with open("tests/testdata/sequence_service_with_all_features.txt") as f:
            expected = f.read().strip()

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        self.assertEqual(result, expected)

    def test_sequence_no_method(self):
        expected = ""

        views_elements = ViewsElements("views.py")
        result = generate_sequence_service_java(
            "burhanpedia", views_elements, "com.example"
        )
        self.assertEqual(result, expected)

    def test_sequence_invalid_param_name(self):
        controller_method_1 = ControllerMethodObject()
        controller_method_1.set_name("controller_method_1")

        param_1 = ParameterObject()
        param_1.set_name("1234")

        controller_method_1.add_parameter(param_1)

        views_elements = ViewsElements("views.py")
        views_elements.add_controller_method(controller_method_1)
        with pytest.raises(ValueError):
            generate_sequence_service_java("burhanpedia", views_elements, "com.example")

    def test_sequence_invalid_controller_method_name(self):
        controller_method_1 = ControllerMethodObject()

        views_elements = ViewsElements("views.py")
        views_elements.add_controller_method(controller_method_1)
        with pytest.raises(ValueError):
            generate_sequence_service_java("burhanpedia", views_elements, "com.example")

    def test_sequence_invalid_return_type(self):
        controller_method_1 = ControllerMethodObject()
        controller_method_1.set_name("controller_method_1")

        type_object = TypeObject()
        type_object.set_name("1ello")

        controller_method_1.set_return_type(type_object)

        views_elements = ViewsElements("views.py")
        views_elements.add_controller_method(controller_method_1)
        with pytest.raises(ValueError):
            generate_sequence_service_java("burhanpedia", views_elements, "com.example")

    def test_sequence_invalid_param_type(self):
        controller_method_1 = ControllerMethodObject()
        controller_method_1.set_name("controller_method_1")

        param_1 = ParameterObject()
        param_1.set_name("hello")

        type_object = TypeObject()
        type_object.set_name("1ello")

        param_1.set_type(type_object)

        controller_method_1.add_parameter(param_1)

        views_elements = ViewsElements("views.py")
        views_elements.add_controller_method(controller_method_1)
        with pytest.raises(ValueError):
            generate_sequence_service_java("burhanpedia", views_elements, "com.example")

    def test_sequence_no_condition(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")
        self.controller_method_1.set_return_type(str_type)

        self.parameter_1 = ParameterObject()
        self.parameter_1.set_name("parameter_1")
        self.parameter_1.set_type(str_type)

        self.controller_method_1.add_parameter(self.parameter_1)

        self.controller_method_call_1 = ControllerMethodCallObject()
        self.controller_method_call_1.set_method(self.controller_method_1)
        self.controller_method_call_1.set_ret_var("ret_var_1")
        self.controller_method_call_1.set_return_var_type(str_type)

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.controller_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.controller_method_call_1.add_argument(self.argument_1)

        self.controller_method_1.add_call(self.controller_method_call_1)

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_return_var_type(str_type)
        self.class_method_call_1.set_instance_name("instance_1")

        self.controller_method_1.add_call(self.class_method_call_1)

        self.views_elements = ViewsElements("SequenceService.java")
        self.views_elements.add_controller_method(self.controller_method_1)

        with open("tests/testdata/sequence_service_no_condition.txt") as f:
            expected = f.read().strip()

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        self.assertEqual(result, expected)

    def test_sequence_no_return_var(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")
        self.controller_method_1.set_return_type(str_type)

        self.parameter_1 = ParameterObject()
        self.parameter_1.set_name("parameter_1")
        self.parameter_1.set_type(str_type)

        self.controller_method_1.add_parameter(self.parameter_1)

        self.controller_method_call_1 = ControllerMethodCallObject()
        self.controller_method_call_1.set_method(self.controller_method_1)
        self.controller_method_call_1.set_condition("condition == True")

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.controller_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.controller_method_call_1.add_argument(self.argument_1)

        self.controller_method_1.add_call(self.controller_method_call_1)

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_instance_name("instance_1")

        self.controller_method_1.add_call(self.class_method_call_1)

        self.views_elements = ViewsElements("SequenceService.java")
        self.views_elements.add_controller_method(self.controller_method_1)

        with open("tests/testdata/sequence_service_no_return_var.txt") as f:
            expected = f.read().strip()

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        self.assertEqual(result, expected)

    def test_sequence_no_parameter(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")
        self.controller_method_1.set_return_type(str_type)

        self.controller_method_call_1 = ControllerMethodCallObject()
        self.controller_method_call_1.set_method(self.controller_method_1)
        self.controller_method_call_1.set_condition("condition == True")
        self.controller_method_call_1.set_ret_var("ret_var_1")
        self.controller_method_call_1.set_return_var_type(str_type)

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.controller_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.controller_method_call_1.add_argument(self.argument_1)

        self.controller_method_1.add_call(self.controller_method_call_1)

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_return_var_type(str_type)
        self.class_method_call_1.set_instance_name("instance_1")

        self.controller_method_1.add_call(self.class_method_call_1)

        self.views_elements = ViewsElements("SequenceService.java")
        self.views_elements.add_controller_method(self.controller_method_1)

        with open("tests/testdata/sequence_service_no_parameter.txt") as f:
            expected = f.read().strip()

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        self.assertEqual(result, expected)

    def test_sequence_no_argument(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")
        self.controller_method_1.set_return_type(str_type)

        self.parameter_1 = ParameterObject()
        self.parameter_1.set_name("parameter_1")
        self.parameter_1.set_type(str_type)

        self.controller_method_1.add_parameter(self.parameter_1)

        self.controller_method_call_1 = ControllerMethodCallObject()
        self.controller_method_call_1.set_method(self.controller_method_1)
        self.controller_method_call_1.set_condition("condition == True")
        self.controller_method_call_1.set_ret_var("ret_var_1")
        self.controller_method_call_1.set_return_var_type(str_type)

        self.controller_method_1.add_call(self.controller_method_call_1)

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_return_var_type(str_type)
        self.class_method_call_1.set_instance_name("instance_1")

        self.controller_method_1.add_call(self.class_method_call_1)

        self.views_elements = ViewsElements("SequenceService.java")
        self.views_elements.add_controller_method(self.controller_method_1)

        with open("tests/testdata/sequence_service_no_argument.txt") as f:
            expected = f.read().strip()

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        self.assertEqual(result, expected)

    def test_sequence_multiple_everything(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.parameter_1 = ParameterObject()
        self.parameter_1.set_name("parameter_1")
        self.parameter_1.set_type(str_type)

        self.class_method_1.add_parameter(self.parameter_1)
        self.class_method_1.add_parameter(self.parameter_1)
        self.class_method_1.add_parameter(self.parameter_1)
        self.class_method_1.add_parameter(self.parameter_1)
        self.class_method_1.add_parameter(self.parameter_1)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_return_var_type(str_type)
        self.class_method_call_1.set_instance_name("instance_1")

        self.class_method_call_2 = ClassMethodCallObject()
        self.class_method_call_2.set_method(self.class_method_1)
        self.class_method_call_2.set_ret_var("ret_var_1")
        self.class_method_call_2.set_instance_name("instance_1")
        self.class_method_call_2.set_return_var_type(str_type)

        self.class_method_call_3 = ClassMethodCallObject()
        self.class_method_call_3.set_method(self.class_method_1)
        self.class_method_call_3.set_condition("condition == True")
        self.class_method_call_3.set_instance_name("instance_1")

        self.class_method_call_4 = ClassMethodCallObject()
        self.class_method_call_4.set_method(self.class_method_1)

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.class_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.class_method_call_1.add_argument(self.argument_1)
        self.class_method_call_1.add_argument(self.argument_1)
        self.class_method_call_1.add_argument(self.argument_1)
        self.class_method_call_1.add_argument(self.argument_1)
        self.class_method_call_1.add_argument(self.argument_1)

        self.class_method_1.add_class_method_call(self.class_method_call_1)
        self.class_method_1.add_class_method_call(self.class_method_call_2)
        self.class_method_1.add_class_method_call(self.class_method_call_3)
        self.class_method_1.add_class_method_call(self.class_method_call_4)

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")
        self.controller_method_1.set_return_type(str_type)
        self.controller_method_1.add_parameter(self.parameter_1)
        self.controller_method_1.add_parameter(self.parameter_1)
        self.controller_method_1.add_parameter(self.parameter_1)
        self.controller_method_1.add_parameter(self.parameter_1)

        self.controller_method_1.add_call(self.class_method_call_4)
        self.controller_method_1.add_call(self.class_method_call_3)
        self.controller_method_1.add_call(self.class_method_call_2)
        self.controller_method_1.add_call(self.class_method_call_1)
        self.controller_method_1.add_call(self.class_method_call_4)

        self.views_elements = ViewsElements("views.py")
        self.views_elements.add_class_method(self.class_method_1)
        self.views_elements.add_class_method(self.class_method_1)
        self.views_elements.add_class_method(self.class_method_1)
        self.views_elements.add_controller_method(self.controller_method_1)
        self.views_elements.add_controller_method(self.controller_method_1)
        self.views_elements.add_controller_method(self.controller_method_1)

        with open("tests/testdata/sequence_service_multiple_everything.txt") as f:
            expected = f.read().strip()

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        self.assertEqual(result, expected)
