import unittest
from unittest.mock import MagicMock, patch

from app.generate_frontend.edit.edit_page_views import generate_edit_page_views
from app.models.diagram import ClassObject, FieldObject
from app.models.elements import ModelsElements


class TestEditPageViews(unittest.TestCase):
    def setUp(self):
        self.models_elements = ModelsElements("TestModel")

        self.class_object1 = ClassObject()
        self.class_object1.set_name("Item")
        field1 = FieldObject()
        field1.set_name("name")
        field2 = FieldObject()
        field2.set_name("description")
        field3 = FieldObject()
        field3.set_name("price")
        self.class_object1.add_field(field1)
        self.class_object1.add_field(field2)
        self.class_object1.add_field(field3)

        self.class_object2 = ClassObject()
        self.class_object2.set_name("Product")
        field21 = FieldObject()
        field21.set_name("name")
        field22 = FieldObject()
        field22.set_name("model")
        self.class_object2.add_field(field21)
        self.class_object2.add_field(field22)

        self.models_elements.add_class(self.class_object1)
        self.models_elements.add_class(self.class_object2)

    def test_generate_edit_page_views_valid(self):
        # Positive case when all fields are valid
        result = generate_edit_page_views(self.models_elements)
        self.assertIn("def edit_item(request, id)", result)
        self.assertIn("def edit_product(request, id)", result)
        self.assertIn("item_obj = Item.objects.get(pk=id)", result)
        self.assertIn("ItemForm(request.POST or None, instance=item_obj)", result)
        self.assertIn("product_obj = Product.objects.get(pk=id)", result)
        self.assertIn("ProductForm(request.POST or None, instance=product_obj)", result)

    @patch("app.generate_frontend.edit.edit_page_views.render_template")
    def test_generate_edit_page_views_correct_template_used(
        self, mock_render: MagicMock
    ):
        # Template rendered should be edit_page_views.py.j2, not anything else
        # positive case
        generate_edit_page_views(self.models_elements)
        ctx = {
            "classes": [
                {"name": "Item", "snake_name": "item"},
                {"name": "Product", "snake_name": "product"},
            ]
        }
        mock_render.assert_called_once_with("edit_page_views.py.j2", ctx)

    def test_generate_edit_page_views_no_classes(self):
        # WHen there are no classes, raise a ValueError
        # negative case
        empty_models_elements = ModelsElements("EmptyModel")
        with self.assertRaises(ValueError) as ctx:
            generate_edit_page_views(empty_models_elements)
        self.assertEqual(str(ctx.exception), "Can't create edit views with no class")

    def test_generate_edit_page_views_some_class_empty_fields(self):
        # When there are classes but some of them have no fields,
        # just return an edit_page_views.py with the ones that have fields
        # edge case
        class_object_no_fields = ClassObject()
        class_object_no_fields.set_name("EmptyClass")
        empty_models_elements = ModelsElements("EmptyClassModel")
        empty_models_elements.add_class(class_object_no_fields)
        empty_models_elements.add_class(self.class_object1)

        result = generate_edit_page_views(empty_models_elements)
        self.assertIn("def edit_item(request, id)", result)
        self.assertNotIn("def edit_empty_class_model(request, id)", result)
        self.assertNotIn(
            "empty_class_model_obj = EmptyClassModel.objects.get(pk=id)", result
        )
        self.assertNotIn(
            "EmptyClassModelForm(request.POST or None, instance=empty_class_model_obj)",
            result,
        )

    def test_generate_edit_page_views_all_class_empty_fields(self):
        # When all classes have no fields, then just return empty views
        # with only imports, edge case
        model_obj = ModelsElements("EmptyModel")
        cls_obj1 = ClassObject()
        cls_obj1.set_name("EmptyClassOne")
        cls_obj2 = ClassObject()
        cls_obj2.set_name("EmptyClassTwo")
        model_obj.add_class(cls_obj1)
        model_obj.add_class(cls_obj2)

        result = generate_edit_page_views(model_obj)
        self.assertNotIn("def edit_empty_class_one(request, id)", result)
        self.assertNotIn("def edit_empty_class_two(request, id)", result)

        # Remove assertIn tests since there exists base_views template for
        # the import & there is no need to import directly from the edit template

        # self.assertIn("from .models import *", result)
        # self.assertIn("from .forms import *", result)
