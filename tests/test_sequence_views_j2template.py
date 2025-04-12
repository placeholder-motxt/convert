import os
import unittest

from app.models.elements import ViewsElements
from app.models.methods import (
    ArgumentObject,
    ClassMethodCallObject,
    ClassMethodObject,
    ControllerMethodObject,
)
from app.models.properties import ParameterObject, TypeObject

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestSequenceViewsJinja2Template(unittest.TestCase):
    def setUp(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.parameter_1 = ParameterObject()
        self.parameter_1.set_name("parameter_1")
        self.parameter_1.set_type(str_type)

        self.class_method_1.add_parameter(self.parameter_1)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_instance_name("instance_1")

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.class_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.class_method_call_1.add_argument(self.argument_1)

        self.class_method_1.add_class_method_call(self.class_method_call_1)

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")

        self.views_elements = ViewsElements("views.py")
        self.views_elements.add_class_method(self.class_method_1)
        self.views_elements.add_controller_method(self.controller_method_1)

    def test_class_with_all_features(self):
        with open(os.path.join(TEST_DIR, "sequence_j2.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    str_type = TypeObject()
    str_type.set_name("string")

    class_method_1 = ClassMethodObject()
    class_method_1.set_name("class_method_1")
    class_method_1.set_return_type(str_type)

    parameter_1 = ParameterObject()
    parameter_1.set_name("parameter_1")
    parameter_1.set_type(str_type)

    class_method_1.add_parameter(parameter_1)

    class_method_call_1 = ClassMethodCallObject()
    class_method_call_1.set_method(class_method_1)
    # class_method_call_1.set_condition("condition == True")
    class_method_call_1.set_ret_var("ret_var_1")
    class_method_call_1.set_instance_name("instance_1")

    argument_1 = ArgumentObject()
    argument_1.set_method_object(class_method_call_1)
    argument_1.set_name("argument_1")
    argument_1.set_type(str_type)

    class_method_call_1.add_argument(argument_1)

    class_method_1.add_class_method_call(class_method_call_1)

    controller_method_1 = ControllerMethodObject()
    controller_method_1.set_name("controller_method_1")

    views_elements = ViewsElements("views.py")
    views_elements.add_class_method(class_method_1)
    views_elements.add_controller_method(controller_method_1)

    print(views_elements.print_django_style_template())
