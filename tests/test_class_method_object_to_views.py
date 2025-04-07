import unittest
from unittest import mock

from app.models.methods import ClassMethodObject
from app.models.properties import ParameterObject, TypeObject


class TestClassMethodObjectToViewsCode(unittest.TestCase):
    def setUp(self):
        self.empty_method = ClassMethodObject()

        self.method_with_name = ClassMethodObject()
        self.method_with_name.set_name("method")

        self.method_with_parameters = ClassMethodObject()
        self.method_with_parameters.set_name("method_params")
        self.param = ParameterObject()
        self.param.set_name("param1")
        self.param_type = TypeObject()
        self.param_type.set_name("int")
        self.param.set_type(self.param_type)
        self.method_with_parameters.add_parameter(self.param)

        self.method_with_return_type = ClassMethodObject()
        self.method_with_return_type.set_name("method_rettype")
        self.return_type = TypeObject()
        self.return_type.set_name("str")
        self.method_with_return_type.set_return_type(self.return_type)

        self.method_with_return_type_list = ClassMethodObject()
        self.method_with_return_type_list.set_name("method_rettype")
        return_type = TypeObject()
        return_type.set_name("list[ABC]")
        self.method_with_return_type_list.set_return_type(return_type)

        self.method_full = ClassMethodObject()
        self.method_full.set_name("method_full")
        self.method_full.add_parameter(self.param)
        self.method_full.set_return_type(self.return_type)

    def test_to_views_code_full(self):
        # Should have param and type annotations for it as well as return type
        result = "def method_full(request, instance_name, param1: int) -> str:\n"
        result += "    # TODO: Auto generated function stub\n"
        result += "    raise NotImplementedError('method_full function is not yet implemented')\n"
        result += "    pass\n"
        self.assertEqual(result, self.method_full.to_views_code())

    def test_to_views_code_no_return_type(self):
        # Should have params and its type annotation but no return type
        result = "def method_params(request, instance_name, param1: int):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += "    raise NotImplementedError('method_params function is not yet implemented')\n"
        result += "    pass\n"
        self.assertEqual(result, self.method_with_parameters.to_views_code())

    def test_to_views_code_param_no_type(self):
        # Parameter doesn't have a type somehow
        result = "def method_params(request, instance_name, param1):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += "    raise NotImplementedError('method_params function is not yet implemented')\n"
        result += "    pass\n"
        self.param.set_type(None)
        self.assertEqual(result, self.method_with_parameters.to_views_code())

    def test_to_views_code_no_parameters(self):
        # Should have the return type annotation but no params
        result = "def method_rettype(request, instance_name) -> str:\n"
        result += "    # TODO: Auto generated function stub\n"
        result += "    raise NotImplementedError('method_rettype"
        result += " function is not yet implemented')\n"
        result += "    pass\n"
        self.assertEqual(result, self.method_with_return_type.to_views_code())

    def test_to_views_code_no_params_or_rettype(self):
        # Should only have method name and body but no params except request and instance_name
        # and return type
        result = "def method(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        result += "    pass\n"
        self.assertEqual(result, self.method_with_name.to_views_code())

    def test_to_views_code_rettype_list(self):
        # Should only have method name and body but no params and return type
        result = "def method_rettype(request, instance_name) -> list[ABC]:\n"
        result += "    # TODO: Auto generated function stub\n"
        result += "    raise NotImplementedError('method_rettype function is not yet implemented')"
        result += "\n"
        result += "    pass\n"
        self.assertEqual(result, self.method_with_return_type_list.to_views_code())

    def test_to_views_code_multiple_params(self):
        # All params should appear in order with its type annotation
        param2 = ParameterObject()
        param2.set_name("param2")
        param2_type = TypeObject()
        param2_type.set_name("str")
        param2.set_type(param2_type)
        self.method_with_parameters.add_parameter(param2)

        param3 = ParameterObject()
        param3.set_name("param3")
        param3_type = TypeObject()
        param3_type.set_name("float")
        param3.set_type(param3_type)
        self.method_with_parameters.add_parameter(param3)

        result = "def method_params(request, instance_name, param1: int, param2: str,"
        result += " param3: float):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += "    raise NotImplementedError('method_params function is not yet implemented')\n"
        result += "    pass\n"
        self.assertEqual(result, self.method_with_parameters.to_views_code())

    def test_to_views_code_invalid_method_name(self):
        # Should not happen if the parser catches it
        # If the ClassMethodObject __name attribute is a Python keyword
        # or is not a valid Python identifier, raise a ValueError
        with self.assertRaises(ValueError) as ctx:
            self.empty_method.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid method name ''\n"
            "please consult the user manual document on how to name methods",
        )

        self.method_with_name.set_name("123")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_name.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid method name '123'\n"
            "please consult the user manual document on how to name methods",
        )

        self.method_with_name.set_name("abcd!")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_name.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid method name 'abcd!'\n"
            "please consult the user manual document on how to name methods",
        )

    def test_to_views_code_invalid_param_type(self):
        # Should not happen if parser catches it
        # But if the param type of a ParameterObject inside
        # ClassMethodObject is not a valid Python identifier or
        # is a Python keyword, then return ValueError
        self.param_type.set_name("")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param type ''\n"
            "please consult the user manual document on how to name parameter types",
        )

        self.param_type.set_name("invalid type")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param type 'invalid type'\n"
            "please consult the user manual document on how to name parameter types",
        )

        self.param_type.set_name("123")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param type '123'\n"
            "please consult the user manual document on how to name parameter types",
        )

        self.param_type.set_name("int!@")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param type 'int!@'\n"
            "please consult the user manual document on how to name parameter types",
        )

    def test_to_views_code_invalid_param_name(self):
        # Should not happen if parser catches it
        # But if the param name is not a Python identifier
        # or is a Python keyword, then raise ValueError
        self.param.set_name("123")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param name '123'\n\
please consult the user manual document on how to name parameters",
        )

        self.param.set_name("invalid name")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param name 'invalid name'\n\
please consult the user manual document on how to name parameters",
        )

        self.param.set_name("param_!$")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid param name 'param_!$'\n\
please consult the user manual document on how to name parameters",
        )

    def test_to_views_code_invalid_return_type(self):
        # Should not happen if parser catches it
        # But if the method's return type is not a Python identifier
        # or is a Python keyword, then raise ValueError
        self.return_type.set_name(" ")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_return_type.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid return type: ' '\n "
            "please consult the user manual document on how to name return variables",
        )

        self.return_type.set_name("123")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_return_type.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid return type: '123'\n "
            "please consult the user manual document on how to name return variables",
        )

        self.return_type.set_name("invalid name")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_return_type.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid return type: 'invalid name'\n "
            "please consult the user manual document on how to name return variables",
        )

        self.return_type.set_name("param_!$")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_return_type.to_views_code()
        self.assertEqual(
            str(ctx.exception),
            "Invalid return type: 'param_!$'\n "
            "please consult the user manual document on how to name return variables",
        )

    def test_to_views_code_one_method_call(self):
        self.class_method_object = ClassMethodObject()
        self.class_method_object.set_name("class_method_1")
        class_method_call = mock.Mock()
        class_method_call.print_django_style.return_value = (
            "ret_var1 = method_call1(arg1, arg2)"
        )
        self.class_method_object.add_class_method_call(class_method_call)
        self.assertEqual(
            self.class_method_object.to_views_code(),
            (
                "def class_method_1(request, instance_name):\n"
                "    ret_var1 = method_call1(arg1, arg2)\n"
                "    # TODO: Auto generated function stub\n"
                "    raise NotImplementedError('class_method_1 function is not yet implemented')\n"
                "    pass\n"
            ),
        )

    def test_to_views_code_two_method_calls(self):
        self.class_method_object = ClassMethodObject()
        self.class_method_object.set_name("class_method_1")
        class_method_call1 = mock.Mock()
        class_method_call1.print_django_style.return_value = (
            "ret_var1 = method_call1(arg1, arg2)"
        )
        self.class_method_object.add_class_method_call(class_method_call1)
        class_method_call2 = mock.Mock()
        class_method_call2.print_django_style.return_value = (
            "ret_var2 = method_call2(arg1, arg2)"
        )
        self.class_method_object.add_class_method_call(class_method_call2)
        self.assertEqual(
            self.class_method_object.to_views_code(),
            (
                "def class_method_1(request, instance_name):\n"
                "    ret_var1 = method_call1(arg1, arg2)\n"
                "    ret_var2 = method_call2(arg1, arg2)\n"
                "    # TODO: Auto generated function stub\n"
                "    raise NotImplementedError('class_method_1 function is not yet implemented')\n"
                "    pass\n"
            ),
        )
