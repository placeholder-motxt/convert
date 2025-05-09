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
from app.models.relationship_enum import RelationshipType


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

    def test_set_is_public(self):
        self.class_object.set_is_public(True)
        self.assertTrue(self.class_object._ClassObject__is_public)
        self.class_object.set_is_public(False)
        self.assertFalse(self.class_object._ClassObject__is_public)

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
targetclass = models.OneToOneField('TargetClass', on_delete = models.CASCADE)\n\t\
targetclassFK = models.ForeignKey('TargetClass', on_delete = models.CASCADE)\n\t\
listOfTargetclass = models.ManyToManyField('TargetClass')\n\tpass\n\n\n"
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
            == "\tuser = models.OneToOneField('User', on_delete = models.CASCADE)\n"
        )

    def test_get_methods(self):
        method = ClassMethodObject()
        self.class_object.add_method(method)

        assert self.class_object.get_methods() == [method]

    def test_get_is_public(self):
        model = ClassObject()
        model.set_is_public(True)
        self.assertTrue(model.get_is_public())
        model.set_is_public(False)
        self.assertFalse(model.get_is_public())

    def test_to_models_springboot_context_positive(self):
        self.class_object.set_name("Test Class")
        parent_class = ClassObject()
        parent_class.set_name("Parent Class")
        self.class_object.set_parent(parent_class)

        field = FieldObject()
        field_type = TypeObject()
        field.set_name("field1")
        field_type.set_name("boolean")
        field.set_type(field_type)
        field.set_modifier("private")
        self.class_object.add_field(field)

        relationship = OneToOneRelationshipObject()
        target_class = ClassObject()
        target_class.set_name("Target Class")
        relationship.set_source_class(self.class_object)
        relationship.set_target_class(target_class)
        self.class_object.add_relationship(relationship)
        target_class.add_relationship(relationship)

        context = self.class_object.to_models_springboot_context()

        expected_context = {
            "name": "TestClass",
            "parent": "ParentClass",
            "fields": [field.to_springboot_models_template()],
            "relationships": [relationship.to_springboot_models_template()],
        }

        self.assertEqual(context, expected_context)

    def test_to_models_springboot_context_no_parent(self):
        self.class_object.set_name("Test Class")
        context = self.class_object.to_models_springboot_context()

        expected_context = {
            "name": "TestClass",
            "parent": None,
            "fields": [],
            "relationships": [],
        }

        self.assertEqual(context, expected_context)

    def test_to_models_springboot_context_edge_case_invalid_field(self):
        self.class_object.set_name("Test Class")
        context = self.class_object.to_models_springboot_context()
        expected_context = {
            "name": "TestClass",
            "parent": None,
            "fields": [],
            "relationships": [],
        }
        self.assertEqual(context, expected_context)

    def test_to_models_springboot_context_edge_case_invalid_relationship(self):
        self.class_object.set_name("Test Class")
        context = self.class_object.to_models_springboot_context()
        expected_context = {
            "name": "TestClass",
            "parent": None,
            "fields": [],
            "relationships": [],
        }
        self.assertEqual(context, expected_context)


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

    def test_negative_set_source_class_as_None(self):  # noqa: N802
        with self.assertRaises(ValueError) as context:
            self.relationship_object.set_source_class(None)

        self.assertEqual(
            str(context.exception),
            "Source Class cannot be SET to be None!\n "
            "Relationship in class diagram is wrong",
        )

    def test_negative_set_target_class_as_None(self):  # noqa: N802
        with self.assertRaises(ValueError) as context:
            self.relationship_object.set_target_class(None)

        self.assertEqual(
            str(context.exception),
            "Target Class cannot be SET to be None!\n "
            "Relationship in class diagram is wrong",
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

    def test_set_source_class_own_amount(self):
        self.relationship_object.set_source_class_own_amount("2")
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__sourceClassOwnAmount,
            "2",
        )

    def test_set_target_class_own_amount(self):
        self.relationship_object.set_target_class_own_amount("1")
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__targetClassOwnAmount,
            "1",
        )

    def test_set_relationship_type(self):
        self.relationship_object.set_type(RelationshipType.ASSOCIATION)
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__relation_type,
            RelationshipType.ASSOCIATION,
        )
        self.relationship_object.set_type(RelationshipType.AGGREGATION)
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__relation_type,
            RelationshipType.AGGREGATION,
        )
        self.relationship_object.set_type(RelationshipType.COMPOSITION)
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__relation_type,
            RelationshipType.COMPOSITION,
        )
        self.relationship_object.set_type(RelationshipType.GENERALIZATION)
        self.assertEqual(
            self.relationship_object._AbstractRelationshipObject__relation_type,
            RelationshipType.GENERALIZATION,
        )

    def test_get_source_class(self):
        self.relationship_object.set_source_class(1)
        assert self.relationship_object.get_source_class() == 1

    def test_get_target_class(self):
        self.relationship_object.set_target_class(1)
        assert self.relationship_object.get_target_class() == 1

    def test_get_type(self):
        self.relationship_object.set_type(RelationshipType.COMPOSITION)
        assert self.relationship_object.get_type() == RelationshipType.COMPOSITION


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
            == "targetclass = models.OneToOneField('TargetClass', on_delete = models.CASCADE)"
        )

    def test_one_to_one_relationship_aggregation(self):
        self.one_to_one_relationship.set_source_class(self.source_class)
        self.one_to_one_relationship.set_target_class(self.target_class)
        self.one_to_one_relationship.set_type(RelationshipType.AGGREGATION)
        assert (
            self.one_to_one_relationship.to_models_code()
            == "targetclass = models.OneToOneField('TargetClass', on_delete = models.SET_NULL, "
            "null=True)"
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
            == "targetclassFK = models.ForeignKey('TargetClass', on_delete = models.CASCADE)"
        )

    def test_many_to_one_relationship_aggregation(self):
        self.many_to_one_relationship.set_source_class(self.source_class)
        self.many_to_one_relationship.set_target_class(self.target_class)
        self.many_to_one_relationship.set_type(RelationshipType.AGGREGATION)
        assert (
            self.many_to_one_relationship.to_models_code()
            == "targetclassFK = models.ForeignKey('TargetClass', on_delete = models.SET_NULL,"
            " null=True)"
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
            == "listOfTargetclass = models.ManyToManyField('TargetClass')"
        )

    def test_is_instance_of_abstract_relationship_object(self):
        self.assertIsInstance(
            self.many_to_many_relationship, AbstractRelationshipObject
        )


class TestToSpringbootModelsTemplate(unittest.TestCase):
    def setUp(self):
        self.source_class = ClassObject()
        self.target_class = ClassObject()
        self.source_class.set_name("Source Class")
        self.target_class.set_name("Target Class")

    def test_one_to_one_relationship_positive(self):
        relationship = OneToOneRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        relationship.set_source_class_own_amount("1")
        expected_output = {
            "name": "private TargetClass targetClass;",
            "type": '@OneToOne(mappedBy="source_class")',
            "join": None,
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)

    def test_one_to_one_relationship_positive_2(self):
        relationship = OneToOneRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        relationship.set_source_class_own_amount("1+")
        expected_output = {
            "name": "private TargetClass targetClass;",
            "type": (
                "@OneToOne(cascade = {CascadeType.PERSIST, "
                "CascadeType.MERGE, CascadeType.REMOVE})"
            ),
            "join": '@JoinColumn(name = "source_class_id")',
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)

    def test_many_to_one_relationship_positive(self):
        relationship = ManyToOneRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        relationship.set_source_class_own_amount("1")
        expected_output = {
            "name": "private TargetClass targetClass;",
            "type": '@ManyToOne(mappedBy="source_class_id")\n\t'
            '@JsonIgnoreProperties("source_classs")',
            "join": None,
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)

    def test_many_to_one_relationship_positive_2(self):
        relationship = ManyToOneRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        relationship.set_source_class_own_amount("*")
        expected_output = {
            "name": "private List<TargetClass> targetClasss;",
            "type": "@OneToMany(\n\t\tcascade = {CascadeType.PERSIST, CascadeType.MERGE},\n\t\t"
            "orphanRemoval = true\n)\n\t@JsonIgnore",
            "join": '@JoinColumn(name = "source_class_id")',
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)

    def test_many_to_many_relationship_positive(self):
        relationship = ManyToManyRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        relationship.set_source_class_own_amount("1")
        expected_output = {
            "name": "private List<TargetClass> listOfTargetClasss;",
            "type": (
                "@ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})\n\t"
                "@JsonIgnore"
            ),
            "join": "@JoinTable("
            '\n\t\tname = "source_class_target_class",'
            '\n\t\tjoinColumns = @JoinColumn(name = "source_class_id"),'
            '\n\t\tinverseJoinColumns = @JoinColumn(name = "target_class_id")\n\t)',
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)

    def test_one_to_one_relationship_edge_case_empty_names(self):
        self.source_class.set_name("")
        self.target_class.set_name("")
        relationship = OneToOneRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        relationship.set_source_class_own_amount("1")
        expected_output = {
            "name": "private  ;",
            "type": '@OneToOne(mappedBy="")',
            "join": None,
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)

    def test_many_to_many_relationship_edge_case_empty_names(self):
        self.source_class.set_name("")
        self.target_class.set_name("")
        relationship = ManyToManyRelationshipObject()
        relationship.set_source_class(self.source_class)
        relationship.set_target_class(self.target_class)
        expected_output = {
            "name": "private List<> listOfs;",
            "type": (
                "@ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})\n\t"
                "@JsonIgnore"
            ),
            "join": "@JoinTable("
            '\n\t\tname = "_",'
            '\n\t\tjoinColumns = @JoinColumn(name = "_id"),'
            '\n\t\tinverseJoinColumns = @JoinColumn(name = "_id")\n\t)',
        }
        self.assertEqual(relationship.to_springboot_models_template(), expected_output)


if __name__ == "__main__":
    unittest.main()
