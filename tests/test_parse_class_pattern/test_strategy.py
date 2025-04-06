import unittest

from app.models.diagram import ClassObject
from app.parse_class_pattern.parse_relationship_strategy import (
    ManyToManyStrategy,
    ManyToOneStrategy,
    OneToOneStrategy,
)


class TestRelationshipStrategy(unittest.TestCase):
    def test_one_to_one_strategy(self):
        strategy = OneToOneStrategy()
        edge = {"startLabel": "1", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(edge, class_from, class_to)
        self.assertEqual(len(class_from._ClassObject__relationships), 1)

    def test_many_to_one_strategy(self):
        strategy = ManyToOneStrategy()
        edge = {"startLabel": "*", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(edge, class_from, class_to)
        self.assertEqual(len(class_from._ClassObject__relationships), 1)

    def test_many_to_many_strategy(self):
        strategy = ManyToManyStrategy()
        edge = {"startLabel": "*", "endLabel": "*"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(edge, class_from, class_to)
        self.assertEqual(len(class_from._ClassObject__relationships), 1)


if __name__ == "__main__":
    unittest.main()
