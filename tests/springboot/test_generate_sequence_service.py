import unittest

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


class DebugTests:
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
        self.class_method_call_1.set_instance_name("instance_1")

        self.controller_method_1.add_call(self.class_method_call_1)

        self.views_elements = ViewsElements("SequenceService.java")
        self.views_elements.add_controller_method(self.controller_method_1)

        result = generate_sequence_service_java(
            "burhanpedia", self.views_elements, "com.example"
        )
        print(result)


if __name__ == "__main__":
    debug_tests = DebugTests()
    debug_tests.test_sequence_with_all_features()
