from app.models.diagram import (
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)


class RelationshipStrategy:
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
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
        bidirectional: bool = False,
    ) -> None:
        ro = OneToOneRelationshipObject()
        ro.set_source_class(class_from_id)
        ro.set_target_class(class_to_id)
        ro.set_source_class_own_amount(edge["startLabel"])
        ro.set_target_class_own_amount(edge["endLabel"])
        class_from_id.add_relationship(ro)
        if bidirectional:
            ro2 = OneToOneRelationshipObject()
            ro2.set_source_class(class_to_id)
            ro2.set_target_class(class_from_id)
            ro2.set_source_class_own_amount(edge["endLabel"])
            ro2.set_target_class_own_amount(edge["startLabel"])
            class_to_id.add_relationship(ro2)


class ManyToOneStrategy(RelationshipStrategy):
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
        bidirectional: bool = False,
    ) -> None:
        ro = ManyToOneRelationshipObject()
        start_condition = (
            "*" in edge["startLabel"]
            or "." in edge["startLabel"]
            or (edge["startLabel"].isnumeric() and int(edge["startLabel"]) > 1)
        )

        if start_condition:
            ro.set_source_class_own_amount(edge["startLabel"])
            ro.set_target_class_own_amount(edge["endLabel"])
            ro.set_source_class(class_from_id)
            ro.set_target_class(class_to_id)
            class_from_id.add_relationship(ro)
            if bidirectional:
                ro2 = ManyToOneRelationshipObject()
                ro2.set_source_class_own_amount(edge["endLabel"])
                ro2.set_target_class_own_amount(edge["startLabel"])
                ro2.set_source_class(class_to_id)
                ro2.set_target_class(class_from_id)
                class_to_id.add_relationship(ro2)
        else:
            ro.set_source_class_own_amount(edge["endLabel"])
            ro.set_target_class_own_amount(edge["startLabel"])
            ro.set_source_class(class_to_id)
            ro.set_target_class(class_from_id)
            class_to_id.add_relationship(ro)
            if bidirectional:
                ro2 = ManyToOneRelationshipObject()
                ro2.set_source_class_own_amount(edge["startLabel"])
                ro2.set_target_class_own_amount(edge["endLabel"])
                ro2.set_source_class(class_from_id)
                ro2.set_target_class(class_to_id)
                class_from_id.add_relationship(ro2)


class ManyToManyStrategy(RelationshipStrategy):
    def create_relationship(
        self,
        edge: dict,
        class_from_id: ClassObject,
        class_to_id: ClassObject,
        bidirectional: bool = False,
    ) -> None:
        ro = ManyToManyRelationshipObject()
        ro.set_source_class(class_from_id)
        ro.set_target_class(class_to_id)
        ro.set_source_class_own_amount(edge["startLabel"])
        ro.set_target_class_own_amount(edge["endLabel"])
        class_from_id.add_relationship(ro)
        if bidirectional:
            ro2 = ManyToManyRelationshipObject()
            ro2.set_source_class(class_to_id)
            ro2.set_target_class(class_from_id)
            ro2.set_source_class_own_amount(edge["endLabel"])
            ro2.set_target_class_own_amount(edge["startLabel"])
            class_to_id.add_relationship(ro2)
