import unittest
from abc import ABC

from app.models.diagram import (
    AbstractRelationshipObject,
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)
from app.models.methods import ClassMethodObject
from app.models.properties import FieldObject, TypeObject


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
        expected_output = (
            "Class Object:\n\tname: TestClass\n\t"
            "parent: None\n\tfields:[]\n\t methods: []\n\trelationships: []"
        )
        self.assertEqual(str(self.class_object), expected_output)

    def test_to_models_code(self):
        self.class_object.set_name("ClassTest")

        target_class = ClassObject()

        target_class.set_name("TargetClass")

        one_to_one_relationship = OneToOneRelationshipObject()
        many_to_one_relationship = ManyToOneRelationshipObject()
        many_to_many_relationship = ManyToManyRelationshipObject()

        one_to_one_relationship.set_target_class(target_class)
        many_to_one_relationship.set_target_class(target_class)
        many_to_many_relationship.set_target_class(target_class)

        field = FieldObject()
        field_type = TypeObject()
        field.set_name("field1")
        field_type.set_name("boolean")
        field.set_type(field_type)
        self.class_object.add_field(field)

        field = FieldObject()
        field_type = TypeObject()
        field.set_name("field2")
        field_type.set_name("integer")
        field.set_type(field_type)
        self.class_object.add_field(field)

        self.class_object.add_relationship(one_to_one_relationship)
        self.class_object.add_relationship(many_to_one_relationship)
        self.class_object.add_relationship(many_to_many_relationship)

        assert (
            self.class_object.to_models_code()
            == "class ClassTest(models.Model):\n\t\
field1 = models.BooleanField()\n\tfield2 = models.IntegerField()\n\n\t\
targetclass = models.OneToOneField(TargetClass, on_delete = models.CASCADE)\n\t\
targetclassFK = models.ForeignKey(TargetClass, on_delete = models.CASCADE)\n\t\
listOfTargetclass = models.ManyToManyField(TargetClass, on_delete = models.CASCADE)\n\tpass\n\n\n"
        )

    def test_get_name(self):
        model = ClassObject()
        model.set_name("TestModel")
        assert model.get_name() == "TestModel"

    def test_get_attributes_to_code(self):
        model = ClassObject()
        model.set_name("TestModel")
        field1 = FieldObject()
        field1.set_name("field1")
        type1 = TypeObject()
        type1.set_name("integer")
        field1.set_type(type1)
        model.add_field(field1)
        assert (
            model._ClassObject__get_attributes_to_code()
            == "\tfield1 = models.IntegerField()\n"
        )

    def test_get_relationships_to_code(self):
        model = ClassObject()
        model.set_name("TestModel")
        user = ClassObject()
        user.set_name("User")
        relationship = OneToOneRelationshipObject()
        relationship.set_target_class(user)
        model.add_relationship(relationship)
        assert (
            model._ClassObject__get_relationships_to_code()
            == "\tuser = models.OneToOneField(User, on_delete = models.CASCADE)\n"
        )

    def test_get_methods(self):
        method = ClassMethodObject()
        self.class_object.add_method(method)

        assert self.class_object.get_methods() == [method]


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
        with self.assertRaises(ValueError) as context:
            self.relationship_object.set_source_class(None)

        self.assertEqual(
            str(context.exception), "Source Class cannot be SET to be None!"
        )

    def test_negative_set_target_class_as_None(self):
        with self.assertRaises(ValueError) as context:
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

    def test_set_Source_Class_Own_Amount(self):
        self.relationship_object.setSourceClassOwnAmount("2")
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__sourceClassOwnAmount,
            "2",
        )

    def test_set_Target_Class_Own_Amount(self):
        self.relationship_object.setTargetClassOwnAmount("1")
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__targetClassOwnAmount,
            "1",
        )

    def test_get_source_class(self):
        self.relationship_object.set_source_class(1)
        assert self.relationship_object.get_source_class() == 1

    def test_get_target_class(self):
        self.relationship_object.set_target_class(1)
        assert self.relationship_object.get_target_class() == 1


class TestOneToOneRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.one_to_one_relationship = OneToOneRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()
        self.source_class.set_name("SourceClass")
        self.target_class.set_name("TargetClass")

    def test_one_to_one_relationship(self):
        self.one_to_one_relationship.set_source_class(self.source_class)
        self.one_to_one_relationship.set_target_class(self.target_class)
        assert (
            self.one_to_one_relationship.to_models_code()
            == "targetclass = models.OneToOneField(TargetClass, on_delete = models.CASCADE)"
        )

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(self.one_to_one_relationship, AbstractRelationshipObject)


class TestManyToOneRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.many_to_one_relationship = ManyToOneRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()
        self.source_class.set_name("SourceClass")
        self.target_class.set_name("TargetClass")

    def test_many_to_one_relationship(self):
        self.many_to_one_relationship.set_source_class(self.source_class)
        self.many_to_one_relationship.set_target_class(self.target_class)
        assert (
            self.many_to_one_relationship.to_models_code()
            == "targetclassFK = models.ForeignKey(TargetClass, on_delete = models.CASCADE)"
        )

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(self.many_to_one_relationship, AbstractRelationshipObject)


class TestManyToManyRelationshipObject(unittest.TestCase):
    def setUp(self):
        self.many_to_many_relationship = ManyToManyRelationshipObject()
        self.source_class = ClassObject()
        self.target_class = ClassObject()
        self.source_class.set_name("SourceClass")
        self.target_class.set_name("TargetClass")

    def test_many_to_many_relationship(self):
        self.many_to_many_relationship.set_source_class(self.source_class)
        self.many_to_many_relationship.set_target_class(self.target_class)
        assert (
            self.many_to_many_relationship.to_models_code()
            == "listOfTargetclass = models.ManyToManyField(TargetClass, on_delete = models.CASCADE)"
        )

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(
            self.many_to_many_relationship, AbstractRelationshipObject
        )


if __name__ == "__main__":
    unittest.main()
