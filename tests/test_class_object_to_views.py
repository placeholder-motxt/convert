import unittest

from app.models.diagram import ClassObject
from app.models.methods import ClassMethodObject


class TestClassObjectToViewsCode(unittest.TestCase):
    def setUp(self):
        self.empty_class = ClassObject()
        self.empty_class.set_name("Empty")

        self.class_with_methods = ClassObject()
        self.class_with_methods.set_name("NotEmpty")
        self.method1 = ClassMethodObject()
        self.method1.set_name("method1")
        self.method2 = ClassMethodObject()
        self.method2.set_name("method2")
        self.class_with_methods.add_method(self.method1)
        self.class_with_methods.add_method(self.method2)

    def test_to_views_code_no_methods(self):
        # When ClassObject doesn't have methods, return empty string instead
        self.assertEqual(self.empty_class.to_views_code(), "")

    def test_to_views_code_one_method(self):
        # When there is 1 method, return its stub
        self.empty_class.add_method(self.method1)
        result = "from .models import Empty\n"
        result += "def method1(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method1 function is not yet implemented')\n"
        )
        self.assertEqual(result, self.empty_class.to_views_code())

    def test_to_views_code_multiple_methods(self):
        # When there is multiple methods, return all of their stubs
        code = self.class_with_methods.to_views_code()
        result = "from .models import NotEmpty\n"
        result += "def method1(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method1 function is not yet implemented')\n"
        )
        result += "def method2(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method2 function is not yet implemented')\n"
        )
        self.assertIn("method1", code)
        self.assertIn("method2", code)
        self.assertEqual(result, code)

    def test_to_views_code_class_obj_has_parent_but_no_own_methods(self):
        # The child should not re-create the method stub already
        # generated by the parent nor appear in the imports
        self.empty_class.set_parent(self.class_with_methods)
        result = "from .models import NotEmpty\n"
        result += "def method1(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method1 function is not yet implemented')\n"
        )
        result += "def method2(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method2 function is not yet implemented')\n"
        )
        self.assertEqual(result, self.empty_class.to_views_code())

    def test_to_views_code_class_obj_has_parent_with_own_methods(self):
        # The child should only add its own method stub and not
        # re add the methods from its parent
        self.empty_class.set_parent(self.class_with_methods)
        method3 = ClassMethodObject()
        method3.set_name("method3")
        self.empty_class.add_method(method3)
        result = "from .models import Empty\nfrom .models import NotEmpty\n"
        result += "def method1(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method1 function is not yet implemented')\n"
        )
        result += "def method2(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method2 function is not yet implemented')\n"
        )
        result += "def method3(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method3 function is not yet implemented')\n"
        )
        self.assertEqual(result, self.empty_class.to_views_code())

    def test_to_views_code_class_obj_has_parent_but_no_methods(self):
        # If child has method and parent does not, then there should
        # only be the child's method stub
        self.class_with_methods.set_parent(self.empty_class)
        result = "from .models import NotEmpty\n"
        result += "def method1(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method1 function is not yet implemented')\n"
        )
        result += "def method2(request, instance_name):\n"
        result += "    # TODO: Auto generated function stub\n"
        result += (
            "    raise NotImplementedError('method2 function is not yet implemented')\n"
        )
        self.assertEqual(result, self.class_with_methods.to_views_code())

    def test_to_views_code_invalid_class_name(self):
        # Should not happen if the parser catches it
        # If the ClassObject __name attribute is a Python keyword
        # or is not a valid Python identifier and has methods
        # (not empty), then raise a ValueError
        self.empty_class.set_name(" ")
        with self.assertRaises(ValueError) as ctx:
            self.empty_class.to_views_code()
        self.assertEqual(str(ctx.exception), "Invalid class name:  ")

        self.empty_class.set_name("123")
        with self.assertRaises(ValueError) as ctx:
            self.empty_class.to_views_code()
        self.assertEqual(str(ctx.exception), "Invalid class name: 123")

        self.empty_class.set_name("abcd!^&@")
        with self.assertRaises(ValueError) as ctx:
            self.empty_class.to_views_code()
        self.assertEqual(str(ctx.exception), "Invalid class name: abcd!^&@")


if __name__ == "__main__":
    unittest.main()
