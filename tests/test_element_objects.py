import unittest
from app.element_objects import ClassObject, FieldObject, ClassMethodObject, RelationshipObject, \
    TypeObject, OneToOneRelationshipObject, ManyToOneRelationshipObject

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
    

        

if __name__ == "__main__":
    unittest.main()
