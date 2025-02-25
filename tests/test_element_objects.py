import unittest
from app.element_objects import *

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
        relationship = RelationshipObject()
        self.class_object.add_relationship(relationship)
        self.assertIn(relationship, self.class_object._ClassObject__relationships)

    def test_str_representation(self):
        self.class_object.set_name("TestClass")
        expected_output = """Class Object:\n\tname: TestClass\n\tparent: None\n\tfields:[]\n\t methods: []\n\trelationships: []"""
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

class TestRelationshipObject(unittest.TestCase):

    def setUp(self):
        self.relationship_object = RelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

        self.source_class.set_name("SourceClass")
        self.target_class.set_name("TargetClass")
    
    def test_positive_set_sourceClass(self):
        self.relationship_object.setSourceClass(self.source_class)
        self.assertEqual(self.relationship_object._RelationshipObject__sourceClass, self.source_class)

    def test_positive_set_targetClass(self):
        self.relationship_object.setTargetClass(self.target_class)
        self.assertEqual(self.relationship_object._RelationshipObject__targetClass, self.target_class)
    
    def test_negative_set_sourceClass_as_None(self):
        with self.assertRaises(Exception) as context:
            self.relationship_object.setSourceClass(None)

        self.assertEqual(str(context.exception), "Source Class cannot be SET to be None!")
    
    def test_negative_set_targetClass_as_None(self):
        with self.assertRaises(Exception) as context:
            self.relationship_object.setTargetClass(None)

        self.assertEqual(str(context.exception), "Target Class cannot be SET to be None!")
    
    def test_edge_source_equals_target(self):
        self.relationship_object.setSourceClass(self.source_class)
        self.relationship_object.setTargetClass(self.source_class)

        self.assertEqual(self.relationship_object._RelationshipObject__sourceClass, self.source_class)
        self.assertEqual(self.relationship_object._RelationshipObject__targetClass, self.source_class)
        
        
class TestAbstractMethodObject(unittest.TestCase):
    def setUp(self):
        self.method_object = AbstractMethodObject()

    def test_set_name(self):
        self.method_object.set_name("TestMethod")
        self.assertEqual(self.method_object._AbstractMethodObject__name, "TestMethod")

    def test_add_parameter(self):
        parameter = ParameterObject()
        self.method_object.add_parameter(parameter)
        self.assertIn(parameter, self.method_object._AbstractMethodObject__parameters)

    def test_set_returnType(self):
        return_type = TypeObject()
        self.method_object.set_returnType(return_type)
        self.assertEqual(self.method_object._AbstractMethodObject__returnType, return_type)

    def test_str_representation(self):
        self.method_object.set_name("TestMethod")
        expected_output = """MethodObject:\n\tname: TestMethod\n\tparameters: []\n\treturnType: None"""
        self.assertEqual(str(self.method_object), expected_output)

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

class TestAbstractMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.method_call_object = AbstractMethodCallObject()

    def test_set_method(self):
        method = AbstractMethodObject()
        self.method_call_object.set_method(method)
        self.assertEqual(self.method_call_object._AbstractMethodCallObject__method, method)

    def test_add_argument(self):
        argument = ArgumentObject()
        self.method_call_object.add_argument(argument)
        self.assertEqual(self.method_call_object._AbstractMethodCallObject__arguments, [argument])

    def test_return_var_name(self):
        self.method_call_object.set_returnVarName("TestVarName")
        self.assertEqual(self.method_call_object._AbstractMethodCallObject__returnVarName, "TestVarName")

    def test_str_representation(self):
        expected_output = """MethodCallObject:\n\tmethod: None\n\targuments: []\n\treturnVarName: """
        self.assertEqual(str(self.method_call_object), expected_output)


class TestOneToOneRelationshipObject(unittest.TestCase):

    def setUp(self):
        self.one_to_one_relationship = OneToOneRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

class TestManyToOneRelationshipObject(unittest.TestCase):

    def setUp(self):
        self.one_to_one_relationship = ManyToOneRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

class TestManyToManyRelationshipObject(unittest.TestCase):

    def setUp(self):
        self.one_to_one_relationship = ManyToManyRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()
    

        
class TestAbstractMethodObject(unittest.TestCase):
    def setUp(self):
        self.method_object = AbstractMethodObject()

    def test_set_name(self):
        self.method_object.set_name("TestMethod")
        self.assertEqual(self.method_object._AbstractMethodObject__name, "TestMethod")

    def test_add_parameter(self):
        parameter = ParameterObject()
        self.method_object.add_parameter(parameter)
        self.assertIn(parameter, self.method_object._AbstractMethodObject__parameters)

    def test_set_returnType(self):
        return_type = TypeObject()
        self.method_object.set_returnType(return_type)
        self.assertEqual(self.method_object._AbstractMethodObject__returnType, return_type)

    def test_str_representation(self):
        self.method_object.set_name("TestMethod")
        expected_output = """MethodObject:\n\tname: TestMethod\n\tparameters: []\n\treturnType: None"""
        self.assertEqual(str(self.method_object), expected_output)

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

class TestAbstractMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.method_call_object = AbstractMethodCallObject()

    def test_set_method(self):
        method = AbstractMethodObject()
        self.method_call_object.set_method(method)
        self.assertEqual(self.method_call_object._AbstractMethodCallObject__method, method)

    def test_add_argument(self):
        argument = ArgumentObject()
        self.method_call_object.add_argument(argument)
        self.assertEqual(self.method_call_object._AbstractMethodCallObject__arguments, [argument])

    def test_return_var_name(self):
        self.method_call_object.set_returnVarName("TestVarName")
        self.assertEqual(self.method_call_object._AbstractMethodCallObject__returnVarName, "TestVarName")

    def test_str_representation(self):
        expected_output = """MethodCallObject:\n\tmethod: None\n\targuments: []\n\treturnVarName: """
        self.assertEqual(str(self.method_call_object), expected_output)

if __name__ == "__main__":
    unittest.main()
