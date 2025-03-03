import unittest
from abc import ABC
from unittest import mock

from app.element_objects import (
    AbstractMethodCallObject,
    AbstractMethodObject,
    AbstractRelationshipObject,
    ArgumentObject,
    ClassMethodCallObject,
    ClassMethodObject,
    ClassObject,
    ControllerMethodCallObject,
    ControllerMethodObject,
    FieldObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    ModelsElements,
    OneToOneRelationshipObject,
    ParameterObject,
    TypeObject,
    ViewsElements,
)


class TestClassObject(unittest.TestCase):
    def setUp(self):
        self.class_object = ClassObject()

    def test_set_name(self):
        self.class_object.set_name("TestClass")
        self.assertEqual(self.class_object._ClassObject__name, "TestClass")

    def test_set_parent(self):
        parent_class = ClassObject()
        self.class_object.set_parent(parent_class)
        self.assertEqual(self.class_object._ClassObject__parent, parent_class)

    def test_add_field(self):
        field = FieldObject()
        self.class_object.add_field(field)
        self.assertIn(field, self.class_object._ClassObject__fields)

    def test_add_method(self):
        method = ClassMethodObject()
        self.class_object.add_method(method)
        self.assertIn(method, self.class_object._ClassObject__methods)

    def test_add_relationship(self):
        relationship = AbstractRelationshipObject()
        self.class_object.add_relationship(relationship)
        self.assertIn(relationship, self.class_object._ClassObject__relationships)

    def test_str_representation(self):
        self.class_object.set_name("TestClass")
        expected_output = (
            "Class Object:\n\tname: TestClass\n\t"
            "parent: None\n\tfields:[]\n\t methods: []\n\trelationships: []"
        )
        self.assertEqual(str(self.class_object), expected_output)


class TestFieldObject(unittest.TestCase):
    def setUp(self):
        self.field_object = FieldObject()

    def test_set_name(self):
        self.field_object.set_name("TestField")
        self.assertEqual(self.field_object._FieldObject__name, "TestField")

    def test_set_type(self):
        type_obj = TypeObject()
        self.field_object.set_type(type_obj)
        self.assertEqual(self.field_object._FieldObject__type, type_obj)

    def test_str_representation(self):
        self.field_object.set_name("TestField")
        expected_output = """FieldObject:\n\tname: TestField\n\ttype: None"""
        self.assertEqual(str(self.field_object), expected_output)


class TestTypeObject(unittest.TestCase):
    def setUp(self):
        self.type_object = TypeObject()

    def test_set_name(self):
        self.type_object.set_name("TestType")
        self.assertEqual(self.type_object._TypeObject__name, "TestType")


class TestAbstractRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.relationship_object = AbstractRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

        self.source_class.set_name("source_class")
        self.target_class.set_name("target_class")

    def test_instance_of_abc(self):
        self.assertIsInstance(self.relationship_object, ABC)

    def test_positive_set_source_class(self):
        self.relationship_object.set_source_class(self.source_class)
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__source_class,
            self.source_class,
        )

    def test_positive_set_target_class(self):
        self.relationship_object.set_target_class(self.target_class)
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__target_class,
            self.target_class,
        )

    def test_negative_set_source_class_as_None(self):
        with self.assertRaises(Exception) as context:
            self.relationship_object.set_source_class(None)

        self.assertEqual(
            str(context.exception), "Source Class cannot be SET to be None!"
        )

    def test_negative_set_target_class_as_None(self):
        with self.assertRaises(Exception) as context:
            self.relationship_object.set_target_class(None)

        self.assertEqual(
            str(context.exception), "Target Class cannot be SET to be None!"
        )

    def test_edge_source_equals_target(self):
        self.relationship_object.set_source_class(self.source_class)
        self.relationship_object.set_target_class(self.source_class)

        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__source_class,
            self.source_class,
        )
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__target_class,
            self.source_class,
        )


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


class TestParameterObject(unittest.TestCase):
    def setUp(self):
        self.parameter_object = ParameterObject()

    def test_set_name(self):
        self.parameter_object.set_name("TestParameter")
        self.assertEqual(self.parameter_object._ParameterObject__name, "TestParameter")

    def test_set_type(self):
        type_obj = TypeObject()
        self.parameter_object.set_type(type_obj)
        self.assertEqual(self.parameter_object._ParameterObject__type, type_obj)

    def test_str_representation(self):
        self.parameter_object.set_name("TestParameter")
        expected_output = """ParameterObject:\n\tname: TestParameter\n\ttype: None"""
        self.assertEqual(str(self.parameter_object), expected_output)

    def test_get_name(self):
        self.parameter_object.set_name("TestParameter")
        self.assertEqual(self.parameter_object.get_name(), "TestParameter")


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
            f"\treturn_var_name: "
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
        expected_output = "result = mock_method(arg1)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)

    def test_print_django_style_two_arguments(self):
        self.method_call_object.set_return_var_name("result")
        self.method_call_object.add_argument(self.argument_mock1)
        self.method_call_object.add_argument(self.argument_mock2)
        expected_output = "result = mock_method(arg1, arg2)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)

    def test_print_django_style_negative(self):
        self.method_call_object.set_method(None)  # No method set
        with self.assertRaises(AttributeError):
            self.method_call_object.print_django_style()

    def test_print_django_style_corner_case_empty_arguments(self):
        self.method_call_object.set_return_var_name("output")
        expected_output = "output = mock_method()"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)

    def test_print_django_style_with_condition(self):
        self.method_call_object.set_condition("x > 5")
        self.method_call_object.set_return_var_name("value")
        self.method_call_object.add_argument(self.argument_mock1)
        expected_output = "if x > 5:\n\t\tvalue = mock_method(arg1)"
        self.assertEqual(self.method_call_object.print_django_style(), expected_output)


class TestOneToOneRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.one_to_one_relationship = OneToOneRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(self.one_to_one_relationship, AbstractRelationshipObject)


class TestManyToOneRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.many_to_one_relationship = ManyToOneRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(self.many_to_one_relationship, AbstractRelationshipObject)


class TestManyToManyRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.many_to_many_relationship = ManyToManyRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(
            self.many_to_many_relationship, AbstractRelationshipObject
        )


class TestArgumentObject(unittest.TestCase):
    def setUp(self):
        self.argument_object = ArgumentObject()

    def test_set_method_object(self):
        method_object = AbstractMethodObject()
        self.argument_object.set_methodObject(method_object)
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
        self.argument_object.set_methodObject(method_object)
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


class TestClassMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.class_method_call = ClassMethodCallObject()

    def test_positive_set_caller(self):
        method_object = ClassMethodObject()
        self.class_method_call.set_caller(method_object)
        self.assertEqual(
            method_object, self.class_method_call._ClassMethodCallObject__caller
        )

    def test_negative_set_caller_as_none(self):
        with self.assertRaises(Exception) as context:
            self.class_method_call.set_caller(None)

        self.assertEqual(
            str(context.exception), "ClassMethodObject cannot be SET to be None!"
        )


class TestModelsElements(unittest.TestCase):
    def test_models_elements_valid_filename(self):
        obj = ModelsElements("model_file.py")
        self.assertIsInstance(obj, ModelsElements)

    def test_models_elements_invalid_filename_type(self):
        with self.assertRaises(AssertionError):
            ModelsElements(123)  # Invalid type

    def test_models_elements_empty_filename(self):  # cornercase
        with self.assertRaises(AssertionError):
            ModelsElements("")

    def test_print_django_style_not_implemented(self):
        obj = ModelsElements("models.py")
        self.assertIsNone(obj.print_django_style())


class TestViewsElements(unittest.TestCase):
    def setUp(self):
        self.views_elements = ViewsElements("view_file.py")

    def test_instance_of_file_elements(self):
        self.assertIsInstance(self.views_elements, ViewsElements)

    def test_print_django_style_no_methods(self):
        expected_output = ""
        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_one_controller_method(self):
        mock_controller_method = mock.Mock()
        mock_controller_method.print_django_style.return_value = (
            "def sample_controller(request):\n\tpass\n"
        )
        self.views_elements.add_controller_method(mock_controller_method)
        expected_output = "def sample_controller(request):\n\tpass\n"
        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_multiple_controller_methods(self):
        mock_controller_method1 = mock.Mock()
        mock_controller_method1.print_django_style.return_value = (
            "def controller_one(request):\n\tpass\n"
        )
        mock_controller_method2 = mock.Mock()
        mock_controller_method2.print_django_style.return_value = (
            "def controller_two(request):\n\tpass\n"
        )

        self.views_elements.add_controller_method(mock_controller_method1)
        self.views_elements.add_controller_method(mock_controller_method2)

        expected_output = (
            "def controller_one(request):\n"
            "\tpass\n"
            "def controller_two(request):\n"
            "\tpass\n"
        )

        self.assertEqual(self.views_elements.print_django_style(), expected_output)

    def test_print_django_style_with_class_methods_ignored(self):
        mock_class_method = mock.Mock()
        mock_class_method.print_django_style.return_value = (
            "class_method should not be included"
        )
        self.views_elements.add_class_method(mock_class_method)
        expected_output = ""
        self.assertEqual(self.views_elements.print_django_style(), expected_output)


if __name__ == "__main__":
    unittest.main()
