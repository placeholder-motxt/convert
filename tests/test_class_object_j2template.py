import os
import unittest
from unittest.mock import MagicMock, patch

from app.models.diagram import (
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)
from app.models.elements import ModelsElements
from app.models.properties import FieldObject, TypeObject

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestClassObjJinja2Template(unittest.TestCase):
    def setUp(self):
        self.cls_obj = ClassObject()
        self.cls_obj.set_name("Item")

        self.field_obj = FieldObject()
        self.field_obj.set_name("name")

        self.type_obj = TypeObject()
        self.type_obj.set_name("String")

        self.field_obj.set_type(self.type_obj)
        self.cls_obj.add_field(self.field_obj)

        self.models_elements = ModelsElements("models.py")
        self.models_elements.add_class(self.cls_obj)

    def build_class_object(
        self,
        class_name: str,
        parent_name: str | None = None,
        fields: list[dict[str, str]] = [],
        relationships: list[dict[str, str]] = [],
    ) -> ClassObject:
        """
        Helper function to build a ClassObject with the given name, parent, and fields.
        """
        cls_obj = ClassObject()
        cls_obj.set_name(class_name)
        if parent_name is not None:
            parent_obj = ClassObject()
            parent_obj.set_name(parent_name)
            cls_obj.set_parent(parent_obj)

        for field in fields:
            field_obj = FieldObject()
            field_obj.set_name(field["name"])

            type_obj = TypeObject()
            type_obj.set_name(field["type"])
            field_obj.set_type(type_obj)

            cls_obj.add_field(field_obj)

        for relation in relationships:
            relationship_obj = None
            if relation["type"] == "1-1":
                relationship_obj = OneToOneRelationshipObject()
            elif relation["type"] == "1-N":
                relationship_obj = ManyToOneRelationshipObject()
            else:
                relationship_obj = ManyToManyRelationshipObject()

            related_cls_obj = ClassObject()
            related_cls_obj.set_name(relation["name"])
            relationship_obj.set_source_class(cls_obj)
            relationship_obj.set_target_class(related_cls_obj)
            cls_obj.add_relationship(relationship_obj)

        return cls_obj

    @patch("jinja2.Environment.get_template")
    def test_model_correct_template_used(self, mock_get_template: MagicMock):
        self.models_elements.print_django_style_template("models.py.j2")
        mock_get_template.assert_called_once_with("models.py.j2")

    @patch("app.models.elements.render_template")
    def test_render_template_called_with_correct_args(
        self, mock_render_template: MagicMock
    ):
        self.models_elements.print_django_style_template("models.py.j2")
        ctx = {
            "classes": [
                {
                    "name": "Item",
                    "parent": "models.Model",
                    "fields": [
                        {"name": "name", "type": "models.CharField(max_length=255)"}
                    ],
                }
            ]
        }
        mock_render_template.assert_called_once_with("models.py.j2", ctx)

    def test_to_views_template_no_parent_one_field(self):
        with open(os.path.join(TEST_DIR, "simple_model.txt")) as f:
            expected = f.read().strip()
        res = self.models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(res, expected)

    def test_class_without_fields(self):
        with open(os.path.join(TEST_DIR, "class_without_fields.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object("EmptyModel")
        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_class_unknown_field_type(self):
        with open(os.path.join(TEST_DIR, "class_unknown_field_type.txt")) as f:
            expected = f.read().strip()

        field_obj = FieldObject()
        field_obj.set_name("unknown")

        type_obj = TypeObject()
        type_obj.set_name("abcd")

        field_obj.set_type(type_obj)
        self.cls_obj.add_field(field_obj)

        result = self.models_elements.print_django_style_template(
            "models.py.j2"
        ).strip()
        self.assertEqual(result, expected)

    def test_class_with_inheritance(self):
        with open(os.path.join(TEST_DIR, "class_with_inheritance.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="AdminUser",
            parent_name="User",
            fields=[
                {"name": "is_admin", "type": "boolean"},
            ],
        )
        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_one_to_one_relationship(self):
        with open(os.path.join(TEST_DIR, "one_to_one_relationship.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Profile",
            fields=[
                {"name": "bio", "type": "Text"},
            ],
            relationships=[
                {"type": "1-1", "name": "User"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_many_to_one_relationship(self):
        with open(os.path.join(TEST_DIR, "many_to_one_relationship.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Comment",
            fields=[
                {"name": "content", "type": "Text"},
            ],
            relationships=[
                {"type": "1-N", "name": "Post"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_many_to_many_relationship(self):
        with open(os.path.join(TEST_DIR, "many_to_many_relationship.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Course",
            fields=[
                {"name": "title", "type": "String"},
            ],
            relationships=[
                {"type": "N-N", "name": "Student"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_multiple_relationships(self):
        with open(os.path.join(TEST_DIR, "multiple_relationship.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Order",
            fields=[
                {"name": "order_date", "type": "Date"},
            ],
            relationships=[
                {"type": "1-1", "name": "Customer"},
                {"type": "1-N", "name": "Product"},
                {"type": "N-N", "name": "Tag"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_class_with_fields_and_one_relationship(self):
        with open(os.path.join(TEST_DIR, "class_fields_one_relationship.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Profile",
            fields=[
                {"name": "bio", "type": "Text"},
                {"name": "birth_date", "type": "Date"},
            ],
            relationships=[
                {"type": "1-1", "name": "User"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_class_with_fields_and_multiple_relationships(self):
        with open(
            os.path.join(TEST_DIR, "class_fields_multiple_relationships.txt")
        ) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Post",
            fields=[
                {"name": "title", "type": "String"},
                {"name": "content", "type": "Text"},
            ],
            relationships=[
                {"type": "1-N", "name": "Author"},
                {"type": "N-N", "name": "Tag"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_class_with_inheritance_fields_and_relationships(self):
        with open(
            os.path.join(TEST_DIR, "class_inheritance_fields_relationships.txt")
        ) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Order",
            parent_name="BaseOrder",
            fields=[
                {"name": "order_date", "type": "Date"},
                {"name": "total_amount", "type": "Decimal"},
            ],
            relationships=[
                {"type": "1-N", "name": "Customer"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)

    def test_class_with_all_features(self):
        with open(os.path.join(TEST_DIR, "class_with_all_features.txt")) as f:
            expected = f.read().strip()

        cls_obj = self.build_class_object(
            class_name="Product",
            parent_name="Item",
            fields=[
                {"name": "name", "type": "String"},
                {"name": "price", "type": "Decimal"},
            ],
            relationships=[
                {"type": "1-1", "name": "Supplier"},
                {"type": "1-N", "name": "Category"},
                {"type": "N-N", "name": "Tag"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        result = models_elements.print_django_style_template("models.py.j2").strip()
        self.assertEqual(result, expected)


if __name__ == "__main__":

    def build_class_object(
        class_name: str,
        parent_name: str | None = None,
        fields: list[dict[str, str]] = [],
        relationships: list[dict[str, str]] = [],
    ) -> ClassObject:
        """
        Helper function to build a ClassObject with the given name, parent, and fields.
        """
        cls_obj = ClassObject()
        cls_obj.set_name(class_name)
        if parent_name is not None:
            parent_obj = ClassObject()
            parent_obj.set_name(parent_name)
            cls_obj.set_parent(parent_obj)

        for field in fields:
            field_obj = FieldObject()
            field_obj.set_name(field["name"])

            type_obj = TypeObject()
            type_obj.set_name(field["type"])
            field_obj.set_type(type_obj)

            cls_obj.add_field(field_obj)

        for relation in relationships:
            relationship_obj = None
            if relation["type"] == "1-1":
                relationship_obj = OneToOneRelationshipObject()
            elif relation["type"] == "1-N":
                relationship_obj = ManyToOneRelationshipObject()
            else:
                relationship_obj = ManyToManyRelationshipObject()

            related_cls_obj = ClassObject()
            related_cls_obj.set_name(relation["name"])
            relationship_obj.set_source_class(cls_obj)
            relationship_obj.set_target_class(related_cls_obj)
            cls_obj.add_relationship(relationship_obj)

        return cls_obj

    with open(os.path.join(TEST_DIR, "class_with_all_features.txt")) as f:
        expected = f.read().strip()

        cls_obj = build_class_object(
            class_name="Product",
            parent_name="Item",
            fields=[
                {"name": "name", "type": "String"},
                {"name": "price", "type": "Decimal"},
            ],
            relationships=[
                {"type": "1-1", "name": "Supplier"},
                {"type": "1-N", "name": "Category"},
                {"type": "N-N", "name": "Tag"},
            ],
        )

        models_elements = ModelsElements("models.py")
        models_elements.add_class(cls_obj)

        i = 0
        for class_object in models_elements.get_classes():
            i += 1
            print(i)

        result = models_elements.print_django_style_template("models.py.j2")
        print(result)
