import unittest

from app.models.diagram import (
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)
from app.models.relationship_enum import RelationshipType
from app.parse_class_pattern.parse_relationship_strategy import (
    ManyToManyStrategy,
    ManyToOneStrategy,
    OneToOneStrategy,
    RelationshipStrategy,
)


class TestRelationshipStrategy(unittest.TestCase):
    def test_one_to_one_strategy(self):
        strategy = OneToOneStrategy()
        edge = {"startLabel": "1", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)

    def test_many_to_one_strategy(self):
        strategy = ManyToOneStrategy()
        edge = {"startLabel": "*", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)

    def test_many_to_many_strategy(self):
        strategy = ManyToManyStrategy()
        edge = {"startLabel": "*", "endLabel": "*"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)

    def test_base_strategy_class_not_implemented_method(self):
        strategy = RelationshipStrategy()
        with self.assertRaises(NotImplementedError) as ctx:
            strategy.create_relationship(
                {}, ClassObject(), ClassObject(), RelationshipType.ASSOCIATION
            )

        self.assertEqual(
            str(ctx.exception),
            "RelationshipStrategy does not implement create_relationship",
        )

    def test_one_to_one_aggregation(self):
        strategy = OneToOneStrategy()
        edge = {"startLabel": "1", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.AGGREGATION
        )
        self.assertEqual(len(class_to._ClassObject__relationships), 1)
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_type(),
            RelationshipType.AGGREGATION,
        )
        self.assertEqual(
            type(class_to._ClassObject__relationships[0]), OneToOneRelationshipObject
        )

    def test_many_to_many_aggregation(self):
        strategy = ManyToManyStrategy()
        edge = {"startLabel": "*", "endLabel": "*"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.AGGREGATION
        )
        self.assertEqual(len(class_to._ClassObject__relationships), 1)
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_type(),
            RelationshipType.AGGREGATION,
        )
        self.assertEqual(
            type(class_to._ClassObject__relationships[0]), ManyToManyRelationshipObject
        )

    def test_many_to_one_aggregation(self):
        strategy = ManyToOneStrategy()
        edge = {"startLabel": "1", "endLabel": "*"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.AGGREGATION
        )
        self.assertEqual(len(class_to._ClassObject__relationships), 1)
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_type(),
            RelationshipType.AGGREGATION,
        )
        self.assertEqual(
            type(class_to._ClassObject__relationships[0]), ManyToOneRelationshipObject
        )

    def test_many_to_one_aggregation_invalid(self):
        strategy = ManyToOneStrategy()
        edge = {"startLabel": "*", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        with self.assertRaises(ValueError):
            strategy.create_relationship(
                edge, class_from, class_to, RelationshipType.AGGREGATION
            )


class TestRelationshipStrategyBidirectional(unittest.TestCase):
    def test_one_to_one_bidirectional(self):
        strategy = OneToOneStrategy()
        edge = {"startLabel": "1", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION, bidirectional=True
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)
        self.assertEqual(
            class_from._ClassObject__relationships[0].get_target_class(), class_to
        )
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_target_class(), class_from
        )

    def test_many_to_one_bidirectional(self):
        strategy = ManyToOneStrategy()
        edge = {"startLabel": "*", "endLabel": "1"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION, bidirectional=True
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)
        self.assertEqual(
            class_from._ClassObject__relationships[0].get_target_class(), class_to
        )
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_target_class(), class_from
        )

    def test_one_to_many_bidirectional(self):
        strategy = ManyToOneStrategy()
        edge = {"startLabel": "1", "endLabel": "*"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION, bidirectional=True
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)
        self.assertEqual(
            class_from._ClassObject__relationships[0].get_target_class(), class_to
        )
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_target_class(), class_from
        )

    def test_many_to_many_bidirectional(self):
        strategy = ManyToManyStrategy()
        edge = {"startLabel": "*", "endLabel": "*"}
        class_from = ClassObject()
        class_to = ClassObject()

        strategy.create_relationship(
            edge, class_from, class_to, RelationshipType.ASSOCIATION, bidirectional=True
        )
        self.assertEqual(len(class_from._ClassObject__relationships), 1)
        self.assertEqual(
            class_from._ClassObject__relationships[0].get_target_class(), class_to
        )
        self.assertEqual(
            class_to._ClassObject__relationships[0].get_target_class(), class_from
        )


if __name__ == "__main__":
    unittest.main()
