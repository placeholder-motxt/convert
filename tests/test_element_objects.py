import unittest
from app.element_objects import ClassObject, FieldObject, ClassMethodObject, RelationshipObject

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

if __name__ == "__main__":
    unittest.main()
