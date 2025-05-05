import unittest
from copy import copy, deepcopy
from unittest.mock import MagicMock, patch

from app.models.properties import (
    FieldObject,
    ParameterObject,
    TypeObject,
)


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

    def test_to_models_code_boolean(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("boolean")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.BooleanField()"

    def test_to_models_code_string(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("String")
        field_object.set_type(type_obj)
        assert (
            field_object.to_models_code()
            == "test_field = models.CharField(max_length=255)"
        )

    def test_to_models_code_integer(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("integer")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.IntegerField()"

    def test_to_models_code_float(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("float")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.FloatField()"

    def test_to_models_code_double(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("double")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.FloatField()"

    def test_to_models_code_date(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("Date")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.DateField()"

    def test_to_models_code_datetime(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("DateTime")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.DateField()"

    def test_to_models_code_time(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("Time")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.TimeField()"

    def test_to_models_code_text(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("Text")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.TextField()"

    def test_to_models_code_email(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("Email")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.EmailField()"

    def test_to_models_code_url(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("URL")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.URLField()"

    def test_to_models_code_uuid(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("UUID")
        field_object.set_type(type_obj)
        assert field_object.to_models_code() == "test_field = models.UUIDField()"

    def test_to_models_code_decimal(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("Decimal")
        field_object.set_type(type_obj)
        assert (
            field_object.to_models_code()
            == "test_field = models.DecimalField(max_digits=10, decimal_places=2)"
        )

    def test_to_models_code_unknown(self):
        field_object = FieldObject()
        field_object.set_name("test_field")
        type_obj = TypeObject()
        type_obj.set_name("Unknown")
        field_object.set_type(type_obj)
        assert (
            field_object.to_models_code()
            == "test_field = models.CharField(max_length=255)"
        )


class TestTypeObject(unittest.TestCase):
    def setUp(self):
        self.type_object = TypeObject()

    def test_set_name(self):
        self.type_object.set_name("TestType")
        self.assertEqual(self.type_object._TypeObject__name, "TestType")

    def test_get_name_springboot_str(self):
        """Test case for 'str' mapped to 'String' in Spring Boot."""
        type_obj = TypeObject()
        type_obj.set_name("string")
        self.assertEqual(type_obj.get_name_springboot(), "String")

    def test_get_name_springboot_int(self):
        """Test case for 'int' mapped to 'int' in Spring Boot."""
        type_obj = TypeObject()
        type_obj.set_name("integer")
        self.assertEqual(type_obj.get_name_springboot(), "int")

    def test_get_name_springboot_bool(self):
        """Test case for 'bool' mapped to 'boolean' in Spring Boot."""
        type_obj = TypeObject()
        type_obj.set_name("boolean")
        self.assertEqual(type_obj.get_name_springboot(), "boolean")

    def test_get_name_springboot_invalid_type(self):
        """Test case for invalid type that should not map to a known Spring Boot type."""
        type_obj = TypeObject()
        type_obj.set_name("float")
        # We expect Error because 'float' does not have a mapping in get_name_springboot
        with self.assertRaises(ValueError):
            type_obj.get_name_springboot()

    def test_get_name_springboot_empty_string(self):
        """Test case for empty string passed as name."""
        type_obj = TypeObject()
        type_obj.set_name("")
        with self.assertRaises(ValueError):
            type_obj.get_name_springboot()  # Empty string maps to None

    def test_get_name_springboot_case_insensitivity(self):
        """Test case for case insensitivity when setting name."""
        type_obj = TypeObject()
        type_obj.set_name("STRING")
        self.assertEqual(type_obj.get_name_springboot(), "String")

    def test_get_name_springboot_non_standard_case(self):
        """Test case for non-standard names, e.g., mixed case strings."""
        type_obj = TypeObject()
        type_obj.set_name("BoOlEan")
        self.assertEqual(type_obj.get_name_springboot(), "boolean")

    def test_get_name_springboot_edge_large_input(self):
        """Test case for handling very large inputs."""
        type_obj = TypeObject()
        type_obj.set_name("a" * 1000)  # Arbitrary large string
        with self.assertRaises(ValueError):
            type_obj.get_name_springboot()


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

    def test_copy(self):
        self.parameter_object.set_name("TestParameter")
        self.parameter_object.set_type("type1")
        temp = copy(self.parameter_object)
        self.assertEqual(temp.get_name(), "TestParameter")
        self.assertEqual(temp._ParameterObject__type, "type1")

    def test_deep_copy(self):
        self.parameter_object.set_name("TestParameter")
        self.parameter_object.set_type("type1")
        temp = deepcopy(self.parameter_object)
        self.assertEqual(temp.get_name(), "TestParameter")
        self.assertEqual(temp._ParameterObject__type, "type1")

    def test_set_modifier_public(self):
        # Positive test case: setting the modifier to "public"
        field_object = FieldObject()
        field_object.set_modifier("public")
        # Assuming that we have a way to access the __modifier value
        # (e.g., a getter or making it public)
        self.assertEqual(field_object._FieldObject__modifier, "public")

    def test_set_modifier_private(self):
        # Positive test case: setting the modifier to "private"
        field_object = FieldObject()
        field_object.set_modifier("private")
        self.assertEqual(field_object._FieldObject__modifier, "private")

    def test_set_modifier_invalid(self):
        # Negative test case: setting the modifier to an invalid value
        field_object = FieldObject()
        with self.assertRaises(ValueError) as context:
            field_object.set_modifier("protected")
        self.assertEqual(
            str(context.exception),
            'Class field modifier must be either "public" or "private" ! Got: protected',
        )

    def test_set_modifier_empty_string(self):
        # Negative test case: setting the modifier to an empty string
        field_object = FieldObject()
        with self.assertRaises(ValueError) as context:
            field_object.set_modifier("")
        self.assertEqual(
            str(context.exception),
            'Class field modifier must be either "public" or "private" ! Got: ',
        )

    def test_set_modifier_none(self):
        # Negative test case: setting the modifier to None
        field_object = FieldObject()
        with self.assertRaises(ValueError) as context:
            field_object.set_modifier(None)
        self.assertEqual(
            str(context.exception),
            'Class field modifier must be either "public" or "private" ! Got: None',
        )

    def test_set_modifier_multiple_calls(self):
        # Corner case: setting modifier to "public" and then "private"
        field_object = FieldObject()
        field_object.set_modifier("public")
        self.assertEqual(field_object._FieldObject__modifier, "public")
        field_object.set_modifier("private")
        self.assertEqual(field_object._FieldObject__modifier, "private")

    # Positive test case where everything is valid
    @patch("app.utils.is_valid_java_identifier", return_value=True)
    def test_valid_param(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name("param1")
        string_type = TypeObject()
        string_type.set_name("string")
        param.set_type(string_type)
        result = param.to_springboot_code_template()
        self.assertEqual(result["param_name"], "param1")
        self.assertEqual(result["param_type"], "String")

    # Negative case when param name is invalid
    @patch("app.utils.is_valid_java_identifier", return_value=False)
    def test_invalid_param_name(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name("invalid param name")
        with self.assertRaises(ValueError):
            param.to_springboot_code_template()

    # Negative case when param type is not standard
    @patch("app.utils.is_valid_java_identifier", return_value=True)
    def test_non_standard_param_type(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name("param1")
        string_type = TypeObject()
        string_type.set_name("hallo")
        param.set_type(string_type)
        with self.assertRaises(ValueError):
            param.to_springboot_code_template()

    # Corner case when param name is None
    @patch("app.utils.is_valid_java_identifier", return_value=False)
    def test_param_name_none(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name(None)
        param.set_type(TypeObject().set_name("string"))
        with self.assertRaises(ValueError):
            param.to_springboot_code_template()

    # Corner case when param name is an empty string
    @patch("app.utils.is_valid_java_identifier", return_value=False)
    def test_empty_param_name(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name("")
        param.set_type(TypeObject().set_name("string"))
        with self.assertRaises(IndexError):
            param.to_springboot_code_template()

    # Test case when param type is None
    @patch("app.utils.is_valid_java_identifier", return_value=True)
    def test_param_type_none(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name("param1")
        param.set_type(None)
        result = param.to_springboot_code_template()
        self.assertEqual(result["param_name"], "param1")
        self.assertNotIn("param_type", result)

    # Test case when param type has a valid mapping (non-None param type)
    @patch("app.utils.is_valid_java_identifier", return_value=True)
    def test_param_type_valid(self, mock_is_valid: MagicMock):
        param = ParameterObject()
        param.set_name("param1")
        string_type = TypeObject()
        string_type.set_name("string")
        param.set_type(string_type)
        result = param.to_springboot_code_template()
        self.assertEqual(result["param_type"], "String")

    # Test case when param type is not valid java identifier
    def test_param_type_invalid_param_type(self):
        param = ParameterObject()
        param.set_name("param1")
        string_type = MagicMock()
        string_type.get_name_springboot.return_value = "&&&"
        param.set_type(string_type)
        with self.assertRaises(ValueError):
            param.to_springboot_code_template()
