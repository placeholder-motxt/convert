from app.models.diagram import (
    AbstractRelationshipObject,
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)
from app.models.relationship_enum import RelationshipType


def _relation_obj_setter_helper(
    ro: AbstractRelationshipObject,
    edge: dict,
    class_from_id: ClassObject,
    class_to_id: ClassObject,
    type: RelationshipType,
    bidirectional: bool = False,
):
    ro.set_type(type)

    # This is for django implementation of aggregation only
    # It needs to be swapped because the "end" on JETUML is the class that is "a part of"
    if ro.get_type() in [
        RelationshipType.AGGREGATION,
        RelationshipType.COMPOSITION,
    ]:
        ro.set_source_class(class_to_id)
        ro.set_target_class(class_from_id)
        ro.set_source_class_own_amount(edge["endLabel"])
        ro.set_target_class_own_amount(edge["startLabel"])
        class_to_id.add_relationship(ro)
        return

    ro.set_source_class(class_from_id)
    ro.set_target_class(class_to_id)
    ro.set_source_class_own_amount(edge["startLabel"])
    ro.set_target_class_own_amount(edge["endLabel"])
    class_from_id.add_relationship(ro)
    if bidirectional:
        ro2 = ManyToManyRelationshipObject()
        ro2.set_source_class(class_to_id)
        ro2.set_target_class(class_from_id)
        ro2.set_source_class_own_amount(edge["startLabel"] + "+")
        ro2.set_target_class_own_amount(edge["endLabel"] + "+")
        class_to_id.add_relationship(ro2)


class RelationshipStrategy:
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
        type: RelationshipType,
        bidirectional: bool = False,
    ) -> None:
        raise NotImplementedError(
            "RelationshipStrategy does not implement create_relationship"
        )


class OneToOneStrategy(RelationshipStrategy):
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
        type: RelationshipType,
        bidirectional: bool = False,
    ) -> None:
        ro = OneToOneRelationshipObject()
        _relation_obj_setter_helper(
            ro, edge, class_from_id, class_to_id, type, bidirectional
        )


class ManyToOneStrategy(RelationshipStrategy):
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
        type: RelationshipType,
        bidirectional: bool = False,
    ) -> None:
        ro = ManyToOneRelationshipObject()
        ro.set_type(type)
        start_condition = (
            "*" in edge["startLabel"]
            or "." in edge["startLabel"]
            or (edge["startLabel"].isnumeric() and int(edge["startLabel"]) > 1)
        )

        if start_condition:
            if ro.get_type() == RelationshipType.AGGREGATION:
                raise ValueError("Aggregation cannot be Many to One")

            ro.set_source_class_own_amount(edge["startLabel"])
            ro.set_target_class_own_amount(edge["endLabel"])
            ro.set_source_class(class_from_id)
            ro.set_target_class(class_to_id)
            class_from_id.add_relationship(ro)
            if bidirectional:
                ro2 = ManyToOneRelationshipObject()
                ro2.set_source_class_own_amount(edge["startLabel"])
                ro2.set_target_class_own_amount(edge["endLabel"])
                ro2.set_source_class(class_to_id)
                ro2.set_target_class(class_from_id)
                class_to_id.add_relationship(ro2)
        else:
            # This is for django implementation of aggregation only
            # It needs to be swapped because the "end" on JETUML is the class that is "a part of"
            if ro.get_type() in [
                RelationshipType.AGGREGATION,
                RelationshipType.COMPOSITION,
            ]:
                ro.set_source_class(class_to_id)
                ro.set_target_class(class_from_id)
                ro.set_source_class_own_amount(edge["endLabel"])
                ro.set_target_class_own_amount(edge["startLabel"])
                class_to_id.add_relationship(ro)
                return

            ro.set_source_class_own_amount(edge["endLabel"])
            ro.set_target_class_own_amount(edge["startLabel"])
            ro.set_source_class(class_to_id)
            ro.set_target_class(class_from_id)
            class_to_id.add_relationship(ro)
            if bidirectional:
                ro2 = ManyToOneRelationshipObject()
                ro2.set_source_class_own_amount(edge["endLabel"])
                ro2.set_target_class_own_amount(edge["startLabel"])
                ro2.set_source_class(class_from_id)
                ro2.set_target_class(class_to_id)
                class_from_id.add_relationship(ro2)


class ManyToManyStrategy(RelationshipStrategy):
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
        type: RelationshipType,
        bidirectional: bool = False,
    ) -> None:
        ro = ManyToManyRelationshipObject()
        _relation_obj_setter_helper(
            ro, edge, class_from_id, class_to_id, type, bidirectional
        )
