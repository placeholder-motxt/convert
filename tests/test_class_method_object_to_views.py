import unittest

from app.element_objects import ClassMethodObject, ParameterObject, TypeObject


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
        self.method_with_return_type.set_returnType(self.return_type)

        self.method_full = ClassMethodObject()
        self.method_full.set_name("method_full")
        self.method_full.add_parameter(self.param)
        self.method_full.set_returnType(self.return_type)

    def test_to_views_code_full(self):
        # Should have param and type annotations for it as well as return type
        result = "def method_full(param1: int) -> str:\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        self.assertEqual(result, self.method_full.to_views_code())

    def test_to_views_code_no_return_type(self):
        # Should have params and its type annotation but no return type
        result = "def method_params(param1: int):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        self.assertEqual(result, self.method_with_parameters.to_views_code())

    def test_to_views_code_no_parameters(self):
        # Should have the return type annotation but no params
        result = "def method_rettype() -> str:\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        self.assertEqual(result, self.method_with_return_type.to_views_code())

    def test_to_views_code_no_params_or_rettype(self):
        # Should only have method name and body but no params and return type
        result = "def method():\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        self.assertEqual(result, self.method_with_name)

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

        result = "def method_params(param1: int, param2: str, param3: float):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method function is not yet implemented')\n"
        )
        self.assertEqual(result, self.method_with_parameters.to_views_code())

    def test_to_views_code_empty_method(self):
        # Should realistically not happen if the parser catches it
        # If the ClassMethodObject for some reason does not have a name or is None, then raise
        # a ValueError
        with self.assertRaises(ValueError) as ctx:
            self.empty_method.to_views_code()
            self.assertEqual(
                str(ctx.exception),
                "ClassMethodObject must have at least a name to generate a function",
            )

    def test_to_views_code_invalid_param_type(self):
        # Should not happen if parser catches it
        # But if the param type of a ParameterObject inside
        # ClassMethodObject is not Python's, a known type, or has whitespaces
        # then return ValueError
        self.param_type.set_name("invalid_type")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
            self.assertEqual(str(ctx.exception), "Invalid type: invalid_type")

        self.param_type.set_name("invalid type")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
            self.assertEqual(str(ctx.exception), "Invalid type: invalid type")

        self.param_type.set_name("123")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
            self.assertEqual(str(ctx.exception), "Invalid type: 123")

        self.param_type.set_name("int!@")
        with self.assertRaises(ValueError) as ctx:
            self.method_with_parameters.to_views_code()
            self.assertEqual(str(ctx.exception), "Invalid type: int!@")
