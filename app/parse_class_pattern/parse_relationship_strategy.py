from app.models.diagram import (
    ClassObject,
    ManyToManyRelationshipObject,
    ManyToOneRelationshipObject,
    OneToOneRelationshipObject,
)


class RelationshipStrategy:
    def create_relationship(
        self, edge: dict, class_from_id: ClassObject, class_to_id: ClassObject
    ) -> None:
        raise NotImplementedError(
            "RelationshipStrategy does not implement create_relationship"
        )


class OneToOneStrategy(RelationshipStrategy):
    def create_relationship(
        self, edge: dict, class_from_id: ClassObject, class_to_id: ClassObject
    ) -> None:
        ro = OneToOneRelationshipObject()
        ro.set_source_class(class_from_id)
        ro.set_target_class(class_to_id)
        ro.set_source_class_own_amount(edge["startLabel"])
        ro.set_target_class_own_amount(edge["endLabel"])
        class_from_id.add_relationship(ro)


class ManyToOneStrategy(RelationshipStrategy):
    def create_relationship(
        self, edge: dict, class_from_id: ClassObject, class_to_id: ClassObject
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
        else:
            ro.set_source_class_own_amount(edge["endLabel"])
            ro.set_target_class_own_amount(edge["startLabel"])
            ro.set_source_class(class_to_id)
            ro.set_target_class(class_from_id)
            class_to_id.add_relationship(ro)


class ManyToManyStrategy(RelationshipStrategy):
    def create_relationship(
        self, edge: dict, class_from_id: ClassObject, class_to_id: ClassObject
    ) -> None:
        ro = ManyToManyRelationshipObject()
        ro.set_source_class(class_from_id)
        ro.set_target_class(class_to_id)
        ro.set_source_class_own_amount(edge["startLabel"])
        ro.set_target_class_own_amount(edge["endLabel"])
        class_from_id.add_relationship(ro)
