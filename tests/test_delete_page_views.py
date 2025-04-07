import unittest

import pytest

from app.generate_frontend.delete.delete_page_views import generate_delete_page_views
from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.models.properties import FieldObject


class TestGeneratedeletePageViews(unittest.TestCase):
    def setUp(self):
        # Prepare models_elements with sample classes and fields
        self.models_elements = ModelsElements("TestModel")

        # First class with fields
        self.class_object1 = ClassObject()
        self.class_object1.set_name("Person")
        field1 = FieldObject()
        field1.set_name("name")
        field2 = FieldObject()
        field2.set_name("age")
        self.class_object1.add_field(field1)
        self.class_object1.add_field(field2)
        self.class_object1.set_is_public(True)
        self.models_elements.add_class(self.class_object1)

        # Second class with fields
        self.class_object2 = ClassObject()
        self.class_object2.set_name("Vehicle")
        field21 = FieldObject()
        field21.set_name("make")
        field22 = FieldObject()
        field22.set_name("model")
        self.class_object2.add_field(field21)
        self.class_object2.add_field(field22)
        self.class_object2.set_is_public(True)
        self.models_elements.add_class(self.class_object2)

        # Objek privat gk bakal ke write sehingga
        # gk bakal mempengaruhi test yang udh ada
        # tapi hanya dengan instansiasi
        # harusnya cukup untuk menguji fungsionalitas
        # write ketika ada private class
        self.class_object3 = ClassObject()
        self.class_object3.set_name("Benda")
        field31 = FieldObject()
        field31.set_name("name")
        field32 = FieldObject()
        field32.set_name("model")
        self.class_object3.add_field(field31)
        self.class_object3.add_field(field32)
        self.class_object3.set_is_public(False)
        self.models_elements.add_class(self.class_object3)

    def test_generate_delete_page_views_positive(self):
        """Test case for valid models_elements"""
        result = generate_delete_page_views(self.models_elements)
        self.assertIn("delete_person", result)
        self.assertIn("delete_vehicle", result)

    def test_generate_delete_page_views_no_classes(self):
        """Test case when no classes are present in models_elements"""
        empty_models_elements = ModelsElements("EmptyModel")
        with pytest.raises(ValueError):
            generate_delete_page_views(empty_models_elements)

    def test_generate_delete_page_views_empty_fields(self):
        """Test case when classes have no fields"""
        class_object_no_fields = ClassObject()
        class_object_no_fields.set_name("EmptyClass")
        empty_models_elements = ModelsElements("EmptyClassModel")
        empty_models_elements.add_class(class_object_no_fields)
        class_object_no_fields.set_is_public(True)
        result = generate_delete_page_views(empty_models_elements)
        self.assertIn("EmptyClass", result)

    def test_generate_delete_page_views_large_number_of_classes(self):
        """Test case for a large number of classes and fields"""
        large_models_elements = ModelsElements("LargeTestModel")
        for i in range(100):
            class_object = ClassObject()
            class_object.set_name(f"Class{i}")
            field = FieldObject()
            field.set_name(f"field{i}")
            class_object.add_field(field)
            class_object.set_is_public(True)
            large_models_elements.add_class(class_object)

        result = generate_delete_page_views(large_models_elements)
        self.assertIn("delete_class99", result)  # Check if the last class is included

    def test_generate_delete_page_views_case_sensitivity(self):
        """Test case for case-sensitive class names"""
        case_sensitive_elements = ModelsElements("CaseSensitiveModel")
        class_object_upper = ClassObject()
        class_object_upper.set_name("Person")
        class_object_lower = ClassObject()
        class_object_lower.set_name("person")
        class_object_lower.set_is_public(True)

        field1 = FieldObject()
        field1.set_name("name")
        class_object_upper.add_field(field1)

        field2 = FieldObject()
        field2.set_name("name")
        class_object_lower.add_field(field2)

        case_sensitive_elements.add_class(class_object_upper)
        case_sensitive_elements.add_class(class_object_lower)

        result = generate_delete_page_views(case_sensitive_elements)
        self.assertIn("delete_person", result)
        self.assertIn(
            "delete_person", result
        )  # Distinct treatment for Person and person


if __name__ == "__main__":
    unittest.main()
