import unittest
from app.element_objects import *

class TestClassObject(unittest.TestCase):

    def setUp(self):
        self.class_object = ClassObject()

    def test_set_id(self):
        self.class_object.set_id(1)
        self.assertEqual(self.class_object._ClassObject__id, 1)

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
        self.relationship_object = AbstractRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()

        self.source_class.set_name("SourceClass")
        self.target_class.set_name("TargetClass")
    
    def test_positive_set_sourceClass(self):
        self.relationship_object.setSourceClass(self.source_class)
        self.assertEqual(self.relationship_object._AbstractRelationshipObject__sourceClass, self.source_class)

    def test_positive_set_targetClass(self):
        self.relationship_object.setTargetClass(self.target_class)
        self.assertEqual(self.relationship_object._AbstractRelationshipObject__targetClass, self.target_class)
    
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

        self.assertEqual(self.relationship_object._AbstractRelationshipObject__sourceClass, self.source_class)
        self.assertEqual(self.relationship_object._AbstractRelationshipObject__targetClass, self.source_class)
        
    def test_set_Source_Class_Own_Amount(self):
        self.relationship_object.setSourceClassOwnAmount("2")
        self.assertEqual(self.relationship_object._AbstractRelationshipObject__sourceClassOwnAmount, "2")
        
    def test_set_Target_Class_Own_Amount(self):
        self.relationship_object.setTargetClassOwnAmount("1")
        self.assertEqual(self.relationship_object._AbstractRelationshipObject__targetClassOwnAmount, "1")
    
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

class TestArgumentObject(unittest.TestCase):
    def setUp(self):
        self.argument_object = ArgumentObject()

    def test_set_method_object(self):
        method_object = AbstractMethodObject()
        self.argument_object.set_methodObject(method_object)
        self.assertEqual(self.argument_object._ArgumentObject__methodObject, method_object)

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
        expected_output = f"""ArgumentObject:\n\tmethodObject: \n\t[MethodObject:\n\tname: TestMethod\n\tparameters: []\n\treturnType: None]\n\tname: TestArgument\n\ttype: \n\t[{self.argument_object._ArgumentObject__type}]"""
        self.assertEqual(str(self.argument_object), expected_output)



class TestControllerMethodCallObject(unittest.TestCase):

    def setUp(self):
        self.controller_method = ControllerMethodCallObject()
        self.class_method = ClassMethodObject()

    def test_set_caller(self):
        self.controller_method.set_caller(self.class_method)
        self.assertEqual(self.controller_method._ControllerMethodCallObject__caller, self.class_method)


class TestControllerMethodObject(unittest.TestCase):

    def setUp(self):
        self.controller_method = ControllerMethodObject()
        self.method_call = AbstractMethodCallObject()

    def test_add_calls(self):
        self.controller_method.add_calls(self.method_call)
        self.assertIn(self.method_call, self.controller_method._ControllerMethodObject__calls)
    
class TestClassMethodObject(unittest.TestCase):
    def setUp(self):
        self.class_method_object = ClassMethodObject()
    
    def test_positive_add_class_method_call_object(self):
        class_method_call_object = ClassMethodCallObject()
        self.class_method_object.add_class_method_call(class_method_call_object)
        self.assertIn(class_method_call_object, self.class_method_object._ClassMethodObject__calls)
    
    def test_negative_add_none(self):
        with self.assertRaises(Exception) as context:
            self.class_method_object.add_class_method_call(None)

        self.assertEqual(str(context.exception), "Cannot add None to ClassMethodCallObject!")

class TestClassMethodCallObject(unittest.TestCase):
    def setUp(self):
        self.class_method_call = ClassMethodCallObject()
    
    def test_positive_set_caller(self):
        method_object = ClassMethodObject()
        self.class_method_call.set_caller(method_object)
        self.assertEqual(method_object, self.class_method_call._ClassMethodCallObject__caller)
    
    def test_negative_set_caller_as_none(self):
        with self.assertRaises(Exception) as context:
            self.class_method_call.set_caller(None)

        self.assertEqual(str(context.exception), "ClassMethodObject cannot be SET to be None!")


if __name__ == "__main__":
    unittest.main()
