from app.models.diagram import (
    AbstractRelationshipObject,
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)
from app.models.relationship_enum import RelationshipType


def __set_attribute_to_relationship(
    ro: AbstractRelationshipObject,
    class_from_id: ClassObject,
    class_to_id: ClassObject,
    source_amount: str,
    target_amount: str,
):
    ro.set_source_class(class_from_id)
    ro.set_target_class(class_to_id)
    ro.set_source_class_own_amount(source_amount)
    ro.set_target_class_own_amount(target_amount)


def __association_django(
    ro: AbstractRelationshipObject,
    class_from_id: ClassObject,
    class_to_id: ClassObject,
    source_amount: str,
    target_amount: str,
):
    __set_attribute_to_relationship(
        ro, class_from_id, class_to_id, source_amount, target_amount
    )
    class_from_id.add_relationship(ro)


def __association_springboot(
    ro: AbstractRelationshipObject,
    class_from_id: ClassObject,
    class_to_id: ClassObject,
    source_amount: str,
    target_amount: str,
):
    if isinstance(ro, OneToOneRelationshipObject):
        ro2 = OneToOneRelationshipObject()
    elif isinstance(ro, ManyToManyRelationshipObject):
        ro2 = ManyToManyRelationshipObject()
    __set_attribute_to_relationship(
        ro2, class_to_id, class_from_id, source_amount, target_amount
    )
    class_to_id.add_relationship(ro2)


def _relation_obj_setter_helper(
    ro: AbstractRelationshipObject,
    edge: dict,
    class_from_id: ClassObject,
    class_to_id: ClassObject,
    relation_type: RelationshipType,
    bidirectional: bool = False,
):
    ro.set_type(relation_type)
    if ro.get_type() in [
        RelationshipType.AGGREGATION,
        RelationshipType.COMPOSITION,
    ]:
        if not bidirectional:
            __set_attribute_to_relationship(
                ro, class_to_id, class_from_id, edge["endLabel"], edge["startLabel"]
            )
            class_to_id.add_relationship(ro)
            return
        if bidirectional:
            if relation_type == RelationshipType.AGGREGATION and isinstance(
                ro, OneToOneRelationshipObject
            ):
                raise ValueError("Aggregation cannot be one to one")
            __set_attribute_to_relationship(
                ro,
                class_from_id,
                class_to_id,
                edge["startLabel"] + "+",
                edge["endLabel"] + "+",
            )
            # ro ownee dikasih ke product
            class_from_id.add_relationship(ro)
            # Set up owner side
            if isinstance(ro, OneToOneRelationshipObject):
                ro2 = OneToOneRelationshipObject()
            elif isinstance(ro, ManyToManyRelationshipObject):
                ro2 = ManyToManyRelationshipObject()
            __set_attribute_to_relationship(
                ro2, class_to_id, class_from_id, edge["endLabel"], edge["startLabel"]
            )
            class_to_id.add_relationship(ro2)
        return

    __association_django(
        ro, class_from_id, class_to_id, edge["startLabel"], edge["endLabel"]
    )
    if bidirectional:
        __association_springboot(
            ro,
            class_from_id,
            class_to_id,
            edge["startLabel"] + "+",
            edge["endLabel"] + "+",
        )


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
                if not bidirectional:
                    ro.set_source_class(class_to_id)
                    ro.set_target_class(class_from_id)
                    ro.set_source_class_own_amount(edge["endLabel"])
                    ro.set_target_class_own_amount(edge["startLabel"])
                    class_to_id.add_relationship(ro)
                    return
                else:
                    ro.set_source_class(class_from_id)
                    ro.set_target_class(class_to_id)

                    # This may look weird but I swear to God don't touch it
                    # this is for UAT quick ducktape fix
                    ro.set_source_class_own_amount(edge["endLabel"])
                    ro.set_target_class_own_amount(edge["startLabel"])
                    #######################################################

                    class_from_id.add_relationship(ro)
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
