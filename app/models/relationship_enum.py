from enum import Enum


class RelationshipType(Enum):
    ASSOCIATION = 1
    AGGREGATION = 2
    COMPOSITION = 3
    GENERALIZATION = 4
