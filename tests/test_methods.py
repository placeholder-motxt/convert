import unittest
from abc import ABC
from unittest import mock

from app.models.methods import (
    AbstractMethodCallObject,
    AbstractMethodObject,
    ArgumentObject,
    ClassMethodCallObject,
    ClassMethodObject,
    ControllerMethodCallObject,
    ControllerMethodObject,
)
from app.models.properties import ParameterObject, TypeObject


class TestAbstractMethodObject(unittest.TestCase):
    def setUp(self):
        self.method_object = AbstractMethodObject()

    def test_abc(self):
        self.assertIsInstance(self.method_object, ABC)

    def test_set_name(self):
        self.method_object.set_name("TestMethod")
        self.assertEqual(self.method_object._AbstractMethodObject__name, "TestMethod")

    def test_add_parameter(self):
        parameter = ParameterObject()
        self.method_object.add_parameter(parameter)
        self.assertIn(parameter, self.method_object._AbstractMethodObject__parameters)

    def test_set_return_type(self):
        return_type = TypeObject()
        self.method_object.set_return_type(return_type)
        self.assertEqual(
            self.method_object._AbstractMethodObject__return_type, return_type
        )

    def test_str_representation(self):
        self.method_object.set_name("TestMethod")
        expected_output = (
            "MethodObject:\n\tname: TestMethod\n\tparameters: []\n\treturn_type: None"
        )
        self.assertEqual(str(self.method_object), expected_output)

    def test_get_name_empty(self):
        self.assertEqual(self.method_object.get_name(), "")

    def test_get_name(self):
        name = "TestMethod"
        self.method_object.set_name(name)
        self.assertEqual(self.method_object.get_name(), name)

    def test_get_parameters_empty(self):
        self.assertEqual(self.method_object.get_parameters(), [])

    def test_get_parameters_with__parameter(self):
        param = ParameterObject()
        self.method_object.add_parameter(param)

        self.assertEqual(self.method_object.get_parameters(), [param])

    def test_get_parameters_with_multiple_parameters(self):
        param1 = ParameterObject()
        param2 = ParameterObject()
        self.method_object.add_parameter(param1)
        self.method_object.add_parameter(param2)
        self.assertEqual(self.method_object.get_parameters(), [param1, param2])


class TestClassMethodObject(unittest.TestCase):
    def setUp(self):
        self.class_method_object = ClassMethodObject()

    def test_positive_add_class_method_call_object(self):
        class_method_call_object = ClassMethodCallObject()
        self.class_method_object.add_class_method_call(class_method_call_object)
        self.assertIn(
            class_method_call_object, self.class_method_object._ClassMethodObject__calls
        )

    def test_negative_add_none(self):
        with self.assertRaises(Exception) as context:
            self.class_method_object.add_class_method_call(None)

        self.assertEqual(
            str(context.exception), "Cannot add None to ClassMethodCallObject!"
        )


class TestControllerMethodObject(unittest.TestCase):
    def setUp(self):
        self.controller_method = ControllerMethodObject()
        self.method_call = AbstractMethodCallObject()

        self.controller_method.get_name = mock.Mock(return_value="sample_method")
        self.controller_method.get_parameters = mock.Mock(return_value=[])

    def test_add_call(self):
        self.controller_method.add_call(self.method_call)
        self.assertIn(
            self.method_call, self.controller_method._ControllerMethodObject__calls
        )

    def test_print_django_style_positive(self):
        mock_call = mock.Mock()
        mock_call.print_django_style.return_value = "mock_call()"
        self.controller_method.add_call(mock_call)
        expected_output = "def sample_method(request):\n\tmock_call()\n\t\n"
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    def test_print_django_style_negative(self):
        self.controller_method.get_name = mock.Mock(return_value="")  # No method name
        with self.assertRaises(TypeError):
            self.controller_method.print_django_style()

    def test_print_django_style_corner_case_empty_parameters(self):
        expected_output = "def sample_method(request):\n\t\n"
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    def test_print_django_style_with_parameters(self):
        param1 = mock.Mock()
        param1.get_name.return_value = "param1"
        param2 = mock.Mock()
        param2.get_name.return_value = "param2"
        self.controller_method.get_parameters = mock.Mock(return_value=[param1, param2])
        expected_output = "def sample_method(request, param1, param2):\n\t\n"
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    def test_print_django_style_with_multiple_calls(self):
        mock_call1 = mock.Mock()
        mock_call1.print_django_style.return_value = "mock_call1()"
        mock_call2 = mock.Mock()
        mock_call2.print_django_style.return_value = "mock_call2()"
        self.controller_method.add_call(mock_call1)
        self.controller_method.add_call(mock_call2)
        expected_output = (
            "def sample_method(request):\n\tmock_call1()\n\tmock_call2()\n\t\n"
        )
        self.assertEqual(self.controller_method.print_django_style(), expected_output)


class TestAbstractMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.method_mock = unittest.mock.Mock()
        self.method_mock.get_name.return_value = "mock_method"
        self.argument_mock1 = unittest.mock.Mock()
        self.argument_mock1.print_django_style.return_value = "arg1"
        self.argument_mock2 = unittest.mock.Mock()
        self.argument_mock2.print_django_style.return_value = "arg2"
        self.method_call_object = AbstractMethodCallObject()
        self.method_call_object.set_method(self.method_mock)

    def test_is_instance_of_abc(self):
        self.assertIsInstance(self.method_call_object, ABC)

    def test_set_method(self):
        method = AbstractMethodObject()
        self.method_call_object.set_method(method)
        self.assertEqual(
            self.method_call_object._AbstractMethodCallObject__method, method
        )

    def test_add_argument(self):
        argument = ArgumentObject()
        self.method_call_object.add_argument(argument)
        self.assertEqual(
            self.method_call_object._AbstractMethodCallObject__arguments, [argument]
        )

    def test_return_var_name(self):
        self.method_call_object.set_return_var_name("TestVarName")
        self.assertEqual(
            self.method_call_object._AbstractMethodCallObject__return_var_name,
            "TestVarName",
        )

    def test_str_representation(self):
        expected_output = (
            f"MethodCallObject:\n"
            f"\tmethod: {self.method_mock}\n"
            f"\targuments: []\n"
            f"\treturn_var_name: \n"
            f"\tcondition: "
        )
        self.assertEqual(str(self.method_call_object), expected_output)

    def test_set_condition(self):
        condition = "True"
        self.method_call_object.set_condition(condition)
        self.assertEqual(
            self.method_call_object._AbstractMethodCallObject__condition, "True"
        )

    def test_print_django_style_one_argument(self):
        self.method_call_object.set_return_var_name("result")
        self.method_call_object.add_argument(self.argument_mock1)
        expected_output = "result = mock_method(request, arg1)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)

    def test_print_django_style_two_arguments(self):
        self.method_call_object.set_return_var_name("result")
        self.method_call_object.add_argument(self.argument_mock1)
        self.method_call_object.add_argument(self.argument_mock2)
        expected_output = "result = mock_method(request, arg1, arg2)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)

    def test_print_django_style_negative(self):
        self.method_call_object.set_method(None)  # No method set
        with self.assertRaises(AttributeError):
            self.method_call_object.print_django_style()

    def test_print_django_style_corner_case_empty_arguments(self):
        self.method_call_object.set_return_var_name("output")
        expected_output = "output = mock_method(request)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)

    def test_print_django_style_with_condition(self):
        self.method_call_object.set_condition("x > 5")
        self.method_call_object.set_return_var_name("value")
        self.method_call_object.add_argument(self.argument_mock1)
        expected_output = "if x > 5:\n\t\tvalue = mock_method(request, arg1)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)


class TestControllerMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.controller_method = ControllerMethodCallObject()
        self.class_method = ClassMethodObject()

    def test_set_caller(self):
        self.controller_method.set_caller(self.class_method)
        self.assertEqual(
            self.controller_method._ControllerMethodCallObject__caller,
            self.class_method,
        )


class TestClassMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.method_mock = unittest.mock.Mock()
        self.method_mock.get_name.return_value = "mock_method"
        self.argument_mock1 = unittest.mock.Mock()
        self.argument_mock1.print_django_style.return_value = "arg1"
        self.argument_mock2 = unittest.mock.Mock()
        self.argument_mock2.print_django_style.return_value = "arg2"
        self.class_method_call_object = ClassMethodCallObject()
        self.class_method_call_object.set_instance_name("instance_name")
        self.class_method_call_object.set_method(self.method_mock)

    def test_positive_set_caller(self):
        method_object = ClassMethodObject()
        self.class_method_call_object.set_caller(method_object)
        self.assertEqual(
            method_object, self.class_method_call_object._ClassMethodCallObject__caller
        )

    def test_negative_set_caller_as_none(self):
        with self.assertRaises(Exception) as context:
            self.class_method_call_object.set_caller(None)

        self.assertEqual(
            str(context.exception), "ClassMethodObject cannot be SET to be None!"
        )

    def test_set_instance_name_valid(self):
        obj = ClassMethodCallObject()
        obj.set_instance_name("valid_instance")
        self.assertEqual(obj._ClassMethodCallObject__instance_name, "valid_instance")

    def test_set_instance_name_empty(self):
        obj = ClassMethodCallObject()
        with self.assertRaises(ValueError) as context:
            obj.set_instance_name("")
        self.assertTrue("instance_name cannot be empty!" in str(context.exception))

    def test_set_instance_name_none(self):
        obj = ClassMethodCallObject()
        with self.assertRaises(ValueError) as context:
            obj.set_instance_name(None)
        self.assertTrue("instance_name cannot be empty!" in str(context.exception))

    def test_get_instance_name_empty(self):
        obj = ClassMethodCallObject()
        self.assertEqual(obj.get_instance_name(), "")

    def test_get_instance_name_set_value(self):
        obj = ClassMethodCallObject()
        obj.set_instance_name("valid_instance")
        self.assertEqual(obj.get_instance_name(), "valid_instance")

    def test_print_django_style_one_argument(self):
        self.class_method_call_object.set_return_var_name("result")
        self.class_method_call_object.add_argument(self.argument_mock1)
        expected_output = "result = mock_method(request, instance_name, arg1)"
        self.assertEqual(
            self.class_method_call_object.print_django_style(), expected_output
        )

    def test_print_django_style_two_arguments(self):
        self.class_method_call_object.set_return_var_name("result")
        self.class_method_call_object.add_argument(self.argument_mock1)
        self.class_method_call_object.add_argument(self.argument_mock2)
        expected_output = "result = mock_method(request, instance_name, arg1, arg2)"
        self.assertEqual(
            self.class_method_call_object.print_django_style(), expected_output
        )

    def test_print_django_style_negative(self):
        self.class_method_call_object.set_method(None)  # No method set
        with self.assertRaises(AttributeError):
            self.class_method_call_object.print_django_style()

    def test_print_django_style_corner_case_empty_arguments(self):
        self.class_method_call_object.set_return_var_name("output")
        expected_output = "output = mock_method(request, instance_name)"
        self.assertEqual(
            self.class_method_call_object.print_django_style(), expected_output
        )

    def test_print_django_style_with_condition(self):
        self.class_method_call_object.set_condition("x > 5")
        self.class_method_call_object.set_return_var_name("value")
        self.class_method_call_object.add_argument(self.argument_mock1)
        expected_output = (
            "if x > 5:\n\t\tvalue = mock_method(request, instance_name, arg1)"
        )
        self.assertEqual(
            self.class_method_call_object.print_django_style(), expected_output
        )


class TestArgumentObject(unittest.TestCase):
    def setUp(self):
        self.argument_object = ArgumentObject()

    def test_set_method_object(self):
        method_object = AbstractMethodObject()
        self.argument_object.set_method_object(method_object)
        self.assertEqual(
            self.argument_object._ArgumentObject__method_object, method_object
        )

    def test_set_name(self):
        self.argument_object.set_name("TestArgument")
        self.assertEqual(self.argument_object._ArgumentObject__name, "TestArgument")

    def test_set_type(self):
        type_obj = TypeObject()
        self.argument_object.set_type(type_obj)
        self.assertEqual(self.argument_object._ArgumentObject__type, type_obj)

    def test_str_representation(self):
        method_object = AbstractMethodObject()
        method_object.set_name("TestMethod")
        self.argument_object.set_method_object(method_object)
        self.argument_object.set_name("TestArgument")
        type_obj = TypeObject()
        type_obj.set_name("TestType")
        self.argument_object.set_type(type_obj)
        expected_output = (
            "ArgumentObject:\n\tmethodObject: \n\t"
            "[MethodObject:\n\tname: TestMethod\n\tparameters: []"
            "\n\treturn_type: None]\n\tname: TestArgument\n\ttype: "
            f"\n\t[{self.argument_object._ArgumentObject__type}]"
            ""
        )
        self.assertEqual(str(self.argument_object), expected_output)

    def test_print_django_style(self):
        test_name = "test_argument"
        self.argument_object.set_name(test_name)
        self.assertEqual(self.argument_object.print_django_style(), test_name)


if __name__ == "__main__":
    unittest.main()
