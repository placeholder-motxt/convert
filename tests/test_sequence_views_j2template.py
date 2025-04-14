import os
import unittest
from unittest.mock import MagicMock, patch

import pytest

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
    def test_sequence_with_all_features(self):
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

        with open(os.path.join(TEST_DIR, "sequence_j2.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    def test_sequence_no_method(self):
        expected = ""

        views_elements = ViewsElements("views.py")
        result = views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    def test_sequence_invalid_class_method_name(self):
        class_method_1 = ClassMethodObject()
        class_method_1.set_name("12334")

        views_elements = ViewsElements("views.py")
        views_elements.add_class_method(class_method_1)
        with pytest.raises(ValueError):
            views_elements.print_django_style_template()

    def test_sequence_invalid_param_name(self):
        class_method_1 = ClassMethodObject()
        class_method_1.set_name("class_method_1")

        param_1 = ParameterObject()
        param_1.set_name("1234")

        class_method_1.add_parameter(param_1)

        views_elements = ViewsElements("views.py")
        views_elements.add_class_method(class_method_1)
        with pytest.raises(ValueError):
            views_elements.print_django_style_template()

    def test_sequence_invalid_controller_method_name(self):
        controller_method_1 = ControllerMethodObject()

        views_elements = ViewsElements("views.py")
        views_elements.add_controller_method(controller_method_1)
        with pytest.raises(ValueError):
            views_elements.print_django_style_template()

    def test_sequence_invalid_return_type(self):
        class_method_1 = ClassMethodObject()
        class_method_1.set_name("class_method_1")

        type_object = TypeObject()
        type_object.set_name("1ello")

        class_method_1.set_return_type(type_object)

        views_elements = ViewsElements("views.py")
        views_elements.add_class_method(class_method_1)
        with pytest.raises(ValueError):
            views_elements.print_django_style_template()

    def test_sequence_list_return_type(self):
        class_method_1 = ClassMethodObject()
        class_method_1.set_name("class_method_1")

        type_object = TypeObject()
        type_object.set_name("list[string]")

        class_method_1.set_return_type(type_object)

        views_elements = ViewsElements("views.py")
        views_elements.add_class_method(class_method_1)

        with open(os.path.join(TEST_DIR, "sequence_j2_list_return_type.txt")) as f:
            expected = f.read().strip()

        result = views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    def test_sequence_invalid_param_type(self):
        class_method_1 = ClassMethodObject()
        class_method_1.set_name("class_method_1")

        param_1 = ParameterObject()
        param_1.set_name("hello")

        type_object = TypeObject()
        type_object.set_name("1ello")

        param_1.set_type(type_object)

        class_method_1.add_parameter(param_1)

        views_elements = ViewsElements("views.py")
        views_elements.add_class_method(class_method_1)
        with pytest.raises(ValueError):
            views_elements.print_django_style_template()

    def test_sequence_no_condition(self):
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
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_instance_name("instance_1")

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.class_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.class_method_call_1.add_argument(self.argument_1)

        self.class_method_1.add_class_method_call(self.class_method_call_1)

        self.views_elements = ViewsElements("views.py")
        self.views_elements.add_class_method(self.class_method_1)

        with open(os.path.join(TEST_DIR, "sequence_j2_no_condition.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    def test_sequence_no_return_var(self):
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
        self.class_method_call_1.set_instance_name("instance_1")

        self.argument_1 = ArgumentObject()
        self.argument_1.set_method_object(self.class_method_call_1)
        self.argument_1.set_name("argument_1")
        self.argument_1.set_type(str_type)

        self.class_method_call_1.add_argument(self.argument_1)

        self.class_method_1.add_class_method_call(self.class_method_call_1)

        self.views_elements = ViewsElements("views.py")
        self.views_elements.add_class_method(self.class_method_1)

        with open(os.path.join(TEST_DIR, "sequence_j2_no_return_var.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    def test_sequence_no_parameter(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

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

        with open(os.path.join(TEST_DIR, "sequence_j2_no_param.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    def test_sequence_no_argument(self):
        str_type = TypeObject()
        str_type.set_name("string")

        self.class_method_1 = ClassMethodObject()
        self.class_method_1.set_name("class_method_1")
        self.class_method_1.set_return_type(str_type)

        self.class_method_call_1 = ClassMethodCallObject()
        self.class_method_call_1.set_method(self.class_method_1)
        self.class_method_call_1.set_condition("condition == True")
        self.class_method_call_1.set_ret_var("ret_var_1")
        self.class_method_call_1.set_instance_name("instance_1")

        self.class_method_1.add_class_method_call(self.class_method_call_1)

        self.controller_method_1 = ControllerMethodObject()
        self.controller_method_1.set_name("controller_method_1")

        self.views_elements = ViewsElements("views.py")
        self.views_elements.add_class_method(self.class_method_1)
        self.views_elements.add_controller_method(self.controller_method_1)

        with open(os.path.join(TEST_DIR, "sequence_j2_no_args.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
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
        self.class_method_call_1.set_instance_name("instance_1")

        self.class_method_call_2 = ClassMethodCallObject()
        self.class_method_call_2.set_method(self.class_method_1)
        self.class_method_call_2.set_ret_var("ret_var_1")
        self.class_method_call_2.set_instance_name("instance_1")

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

        with open(os.path.join(TEST_DIR, "sequence_j2_multiple_everything.txt")) as f:
            expected = f.read().strip()

        result = self.views_elements.print_django_style_template().strip()
        self.assertEqual(result, expected)

    @patch("app.utils.render_template")
    def test_print_django_style_template_exception(
        self, mock_render_template: MagicMock
    ):
        mock_render_template.side_effect = Exception("Test exception")
        your_instance = ViewsElements("views.py")
        result = your_instance.print_django_style_template()
        self.assertEqual(result, "")
