import unittest
from abc import ABC
from unittest import mock
from unittest.mock import MagicMock, patch

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
        with self.assertRaises(ValueError) as context:
            self.class_method_object.add_class_method_call(None)

        self.assertEqual(
            str(context.exception),
            "Cannot add None to ClassMethodCallObject! please consult the user manual document",
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
        expected_output = "def sample_method(request):\n\tmock_call()\n\tpass\n\n"
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    def test_print_django_style_negative(self):
        self.controller_method.get_name = mock.Mock(return_value="")  # No method name
        with self.assertRaises(ValueError):
            self.controller_method.print_django_style()

    def test_print_django_style_corner_case_empty_parameters(self):
        expected_output = "def sample_method(request):\n\tpass\n\n"
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    def test_print_django_style_with_parameters(self):
        param1 = mock.Mock()
        param1.get_name.return_value = "param1"
        param2 = mock.Mock()
        param2.get_name.return_value = "param2"
        self.controller_method.get_parameters = mock.Mock(return_value=[param1, param2])
        expected_output = "def sample_method(request, param1, param2):\n\tpass\n\n"
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    def test_print_django_style_with_multiple_calls(self):
        mock_call1 = mock.Mock()
        mock_call1.print_django_style.return_value = "mock_call1()"
        mock_call2 = mock.Mock()
        mock_call2.print_django_style.return_value = "mock_call2()"
        self.controller_method.add_call(mock_call1)
        self.controller_method.add_call(mock_call2)
        expected_output = (
            "def sample_method(request):\n\tmock_call1()\n\tmock_call2()\n\tpass\n\n"
        )
        self.assertEqual(self.controller_method.print_django_style(), expected_output)

    # Positive Test Case 1: Method with valid name, parameters, and method calls
    @patch.object(
        ParameterObject,
        "to_springboot_code_template",
        return_value={"param_name": "exampleParam"},
    )
    @patch.object(
        AbstractMethodCallObject,
        "print_springboot_style_template",
        return_value={"method_name": "methodCall"},
    )
    def test_valid_method_with_parameters_and_calls(
        self, mock_print_method_call: MagicMock, mock_param_template: MagicMock
    ):
        method_obj = ControllerMethodObject()
        method_obj.set_name("testControllerMethod")

        param1 = ParameterObject()
        method_obj.add_parameter(param1)
        str_type = TypeObject()
        str_type.set_name("string")
        method_obj.set_return_type(str_type)

        # Adding a mock method call
        method_call_mock = AbstractMethodCallObject()
        method_obj.add_call(method_call_mock)

        expected_result = {
            "method_name": "testControllerMethod",
            "params": [{"param_name": "exampleParam"}],
            "method_calls": [{"method_name": "methodCall"}],
            "return_type": "String",
        }

        result = method_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)

    # Negative Test Case 1: Method with empty name
    def test_method_with_empty_name(self):
        method_obj = ControllerMethodObject()
        method_obj.set_name("")

        with self.assertRaises(ValueError) as context:
            method_obj.print_springboot_style_template()

        self.assertEqual(
            str(context.exception),
            "method cannot be empty\nplease consult the user manual document",
        )

    # Negative Test Case 2: Method with invalid parameters
    @patch.object(
        ParameterObject, "to_springboot_code_template", return_value={}
    )  # Mock empty dictionary
    def test_method_with_invalid_parameters(
        self, mock_to_springboot_code_template: MagicMock
    ):
        method_obj = ControllerMethodObject()
        method_obj.set_name("testMethodWithInvalidParams")

        str_type = TypeObject()
        str_type.set_name("string")
        method_obj.set_return_type(str_type)

        param1 = ParameterObject()
        method_obj.add_parameter(param1)

        result = method_obj.print_springboot_style_template()
        expected_result = {
            "method_name": "testMethodWithInvalidParams",
            "params": [{}],  # The parameter's template is invalid (empty dictionary)
            "method_calls": [],  # No method calls
            "return_type": "String",
        }

        self.assertEqual(result, expected_result)

    # Corner Case 1: Method with no parameters
    def test_method_with_no_parameters(self):
        method_obj = ControllerMethodObject()
        method_obj.set_name("testMethodWithNoParams")

        str_type = TypeObject()
        str_type.set_name("string")
        method_obj.set_return_type(str_type)

        expected_result = {
            "method_name": "testMethodWithNoParams",
            "params": [],
            "method_calls": [],  # No method calls
            "return_type": "String",
        }

        result = method_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)

    # Corner Case 2: Method with a very large number of parameters
    @patch.object(
        ParameterObject,
        "to_springboot_code_template",
        return_value={"param_name": "param"},
    )
    def test_method_with_large_number_of_parameters(
        self, mock_to_springboot_code_template: MagicMock
    ):
        method_obj = ControllerMethodObject()
        method_obj.set_name("testMethodWithManyParams")
        str_type = TypeObject()
        str_type.set_name("string")
        method_obj.set_return_type(str_type)

        # Adding 1000 parameters to the method
        for _ in range(1000):
            param = ParameterObject()
            method_obj.add_parameter(param)

        # Only checking the length of params in the result
        result = method_obj.print_springboot_style_template()
        self.assertEqual(len(result["params"]), 1000)


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

    # Positive Test Case 1: Method with valid arguments and a return variable name
    @patch.object(AbstractMethodObject, "get_name", return_value="testMethod")
    @patch.object(
        ArgumentObject, "print_springboot_style_template", return_value={"arg": "value"}
    )
    def test_valid_method_call_with_arguments_and_return_var(
        self, mock_get_name: MagicMock, mock_print_arg: MagicMock
    ):
        method_call_obj = AbstractMethodCallObject()

        # Mocking a method and adding an argument
        method_mock = AbstractMethodObject()
        method_call_obj.set_method(method_mock)
        method_call_obj.set_return_var_name("result")

        str_type = TypeObject()
        str_type.set_name("string")
        method_call_obj.set_return_var_type(str_type)

        method_call_obj.set_condition("if true")

        argument = ArgumentObject()
        method_call_obj.add_argument(argument)

        expected_result = {
            "condition": "if true",
            "return_var_name": "result",
            "method_name": "testMethod",
            "arguments": [{"arg": "value"}],
            "return_var_type": "String",
        }

        result = method_call_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)

    # Positive Test Case 2: ClassMethodCallObject with instance name
    @patch.object(AbstractMethodObject, "get_name", return_value="testMethod")
    @patch.object(
        ArgumentObject, "print_springboot_style_template", return_value={"arg": "value"}
    )
    def test_class_method_call_with_instance_name(
        self, mock_get_name: MagicMock, mock_print_arg: MagicMock
    ):
        method_call_obj = ClassMethodCallObject()
        method_call_obj.set_instance_name("instance1")

        # Mocking a method and adding an argument
        method_mock = AbstractMethodObject()
        method_call_obj.set_method(method_mock)
        method_call_obj.set_return_var_name("result")

        str_type = TypeObject()
        str_type.set_name("string")
        method_call_obj.set_return_var_type(str_type)

        method_call_obj.set_condition("if true")

        argument = ArgumentObject()
        method_call_obj.add_argument(argument)

        expected_result = {
            "condition": "if true",
            "return_var_name": "result",
            "method_name": "testMethod",
            "instance_name": "instance1",
            "arguments": [{"arg": "value"}],
            "return_var_type": "String",
        }

        result = method_call_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)

    # Negative Test Case 1: Method with no arguments and empty return variable name
    @patch.object(AbstractMethodObject, "get_name", return_value="testMethod")
    def test_method_with_no_arguments_and_empty_return_var(
        self, mock_get_name: MagicMock
    ):
        method_call_obj = AbstractMethodCallObject()

        # Mocking a method
        method_mock = AbstractMethodObject()
        method_call_obj.set_method(method_mock)

        expected_result = {"method_name": "testMethod", "arguments": []}

        result = method_call_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)

    # Negative Test Case 2: Method with empty condition
    @patch.object(AbstractMethodObject, "get_name", return_value="testMethod")
    def test_method_with_empty_condition(self, mock_get_name: MagicMock):
        method_call_obj = AbstractMethodCallObject()

        # Mocking a method
        method_mock = AbstractMethodObject()
        method_call_obj.set_method(method_mock)
        method_call_obj.set_return_var_name("result")

        str_type = TypeObject()
        str_type.set_name("string")
        method_call_obj.set_return_var_type(str_type)

        # Setting empty condition
        method_call_obj.set_condition("")

        expected_result = {
            "return_var_name": "result",
            "method_name": "testMethod",
            "arguments": [],
            "return_var_type": "String",
        }

        result = method_call_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)

    # Corner Case: Method with no method, no arguments, no return var name, and no condition
    def test_method_with_no_method_or_arguments(self):
        method_call_obj = AbstractMethodCallObject()
        with self.assertRaises(AttributeError):
            method_call_obj.print_springboot_style_template()

    # Edge Case: Arguments are complex or involve mocked classes
    @patch.object(AbstractMethodObject, "get_name", return_value="testMethod")
    @patch.object(
        ArgumentObject,
        "print_springboot_style_template",
        return_value={"complex_arg": "complex_value"},
    )
    def test_method_with_complex_arguments(
        self, mock_get_name: MagicMock, mock_print_arg: MagicMock
    ):
        method_call_obj = AbstractMethodCallObject()

        # Mocking a method
        method_mock = AbstractMethodObject()
        method_call_obj.set_method(method_mock)
        method_call_obj.set_return_var_name("complex_result")

        str_type = TypeObject()
        str_type.set_name("string")
        method_call_obj.set_return_var_type(str_type)

        method_call_obj.set_condition("if complex")

        complex_argument = ArgumentObject()
        method_call_obj.add_argument(complex_argument)

        expected_result = {
            "condition": "if complex",
            "return_var_name": "complex_result",
            "method_name": "testMethod",
            "arguments": [{"complex_arg": "complex_value"}],
            "return_var_type": "String",
        }

        result = method_call_obj.print_springboot_style_template()
        self.assertEqual(result, expected_result)


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
        with self.assertRaises(ValueError) as context:
            self.class_method_call_object.set_caller(None)

        self.assertEqual(
            str(context.exception),
            "ClassMethodObject cannot be SET to be None!\nplease consult the user manual document",
        )

    def test_set_instance_name_valid(self):
        obj = ClassMethodCallObject()
        obj.set_instance_name("valid_instance")
        self.assertEqual(obj._ClassMethodCallObject__instance_name, "valid_instance")

    def test_set_instance_name_empty(self):
        obj = ClassMethodCallObject()
        with self.assertRaises(ValueError) as context:
            obj.set_instance_name("")
        self.assertIn("instance_name cannot be empty!", str(context.exception))

    def test_set_instance_name_none(self):
        obj = ClassMethodCallObject()
        with self.assertRaises(ValueError) as context:
            obj.set_instance_name(None)
        self.assertIn("instance_name cannot be empty!", str(context.exception))

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

    # Positive Test Case 1: Argument with a valid name
    def test_valid_argument_name(self):
        arg_obj = ArgumentObject()
        arg_obj.set_name("validArgument")
        result = arg_obj.print_springboot_style_template()
        self.assertEqual(result, {"argument_name": "validArgument"})


class TestHandleDuplicateReturnValueNames(unittest.TestCase):
    def setUp(self):
        # This method will be run before each test
        self.method_calls = [
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "output", "return_var_type": "String"},
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "error", "return_var_type": "boolean"},
        ]

    def test_no_duplicates(self):
        method_calls = [
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "output", "return_var_type": "String"},
            {"return_var_name": "error", "return_var_type": "boolean"},
        ]
        controller_method_object = ControllerMethodObject()
        result = controller_method_object.handle_duplicate_return_value_names(
            method_calls
        )
        self.assertEqual(result, method_calls)

    def test_duplicates(self):
        method_calls = [
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "output", "return_var_type": "String"},
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "error", "return_var_type": "boolean"},
        ]
        expected_result = [
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "output", "return_var_type": "String"},
            {"return_var_name": "result", "return_var_type": ""},
            {"return_var_name": "error", "return_var_type": "boolean"},
        ]
        controller_method_object = ControllerMethodObject()
        result = controller_method_object.handle_duplicate_return_value_names(
            method_calls
        )
        self.assertEqual(result, expected_result)

    def test_all_duplicates(self):
        method_calls = [
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "result", "return_var_type": "int"},
        ]
        expected_result = [
            {"return_var_name": "result", "return_var_type": "int"},
            {"return_var_name": "result", "return_var_type": ""},
            {"return_var_name": "result", "return_var_type": ""},
        ]
        controller_method_object = ControllerMethodObject()
        result = controller_method_object.handle_duplicate_return_value_names(
            method_calls
        )
        self.assertEqual(result, expected_result)

    def test_empty_input(self):
        method_calls = []
        controller_method_object = ControllerMethodObject()
        result = controller_method_object.handle_duplicate_return_value_names(
            method_calls
        )
        self.assertEqual(result, [])

    def test_single_element_input(self):
        method_calls = [{"return_var_name": "result", "return_var_type": "int"}]
        controller_method_object = ControllerMethodObject()
        result = controller_method_object.handle_duplicate_return_value_names(
            method_calls
        )
        self.assertEqual(result, method_calls)

    def test_input_with_empty_return_var_type(self):
        method_calls = [
            {"return_var_name": "result", "return_var_type": ""},
            {"return_var_name": "output", "return_var_type": "String"},
            {"return_var_name": "result", "return_var_type": "int"},
        ]
        expected_result = [
            {"return_var_name": "result", "return_var_type": ""},
            {"return_var_name": "output", "return_var_type": "String"},
            {"return_var_name": "result", "return_var_type": ""},
        ]
        controller_method_object = ControllerMethodObject()
        result = controller_method_object.handle_duplicate_return_value_names(
            method_calls
        )
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
