from app.models.relationship_enum import (
    RelationshipType,  # Replace 'your_module' with the actual module name
)


def test_enum_members_exist():
    assert RelationshipType.ASSOCIATION.name == "ASSOCIATION"
    assert RelationshipType.AGGREGATION.name == "AGGREGATION"
    assert RelationshipType.COMPOSITION.name == "COMPOSITION"
    assert RelationshipType.GENERALIZATION.name == "GENERALIZATION"

    assert RelationshipType.ASSOCIATION.value == 1
    assert RelationshipType.AGGREGATION.value == 2
    assert RelationshipType.COMPOSITION.value == 3
    assert RelationshipType.GENERALIZATION.value == 4


def test_enum_member_count():
    members = list(RelationshipType)
    assert len(members) == 4
    assert set(m.name for m in members) == {
        "ASSOCIATION",
        "AGGREGATION",
        "COMPOSITION",
        "GENERALIZATION",
    }
