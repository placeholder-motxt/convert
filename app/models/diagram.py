from __future__ import annotations

from abc import ABC
from io import StringIO
from typing import Optional

from app.utils import is_valid_python_identifier

from .methods import ClassMethodObject
from .properties import FieldObject


class ClassObject:
    """Represents a single JetUML ClassNode."""

    def __init__(self):
        self.__name: str = ""
        self.__parent: Optional[ClassObject] = None
        self.__fields: list[FieldObject] = []
        self.__methods: list[ClassMethodObject] = []
        self.__relationships: list[AbstractRelationshipObject] = []

        self.__id: int

    def to_models_code(self) -> str:
        return (
            f"class {self.__name}"
            + f"({self.__parent.get_name() if self.__parent else 'models.Model'}):"
            + f"\n{self.__get_attributes_to_code()}\n{self.__get_relationships_to_code()}\n"
        )

    def to_views_code(self) -> str:
        if not is_valid_python_identifier(self.__name):
            raise ValueError(f"Invalid class name: {self.__name}")

        res = ""
        if len(self.__methods) > 0:
            res = f"from .models import {self.__name}\n"

        if self.__parent is not None:
            res += self.__parent.to_views_code()

        for method in self.__methods:
            res += method.to_views_code()

        return res

    def __str__(self) -> str:
        """__str__ method for debugging purposes."""
        return (
            f"Class Object:\n\tname: {self.__name}\n\tparent: {self.__parent}"
            f"\n\tfields:{self.__fields}\n\t methods: {self.__methods}"
            f"\n\trelationships: {self.__relationships}"
        )

    def set_name(self, name: str):
        self.__name = name

    def set_parent(self, parent: ClassObject):
        self.__parent = parent

    def add_field(self, field: FieldObject):
        self.__fields.append(field)

    def add_method(self, method: ClassMethodObject):
        self.__methods.append(method)

    def add_relationship(self, relationship: AbstractRelationshipObject):
        self.__relationships.append(relationship)

    def set_id(self, id: int):
        self.__id = id

    def get_name(self) -> str:
        return self.__name
      
    def get_methods(self) -> list[ClassMethodObject]:
        return self.__methods

    def __get_attributes_to_code(self) -> str:
        res = StringIO()
        for attribute in self.__fields:
            res.write("\t" + attribute.to_models_code() + "\n")
        return res.getvalue()

    def __get_relationships_to_code(self) -> str:
        res = StringIO()
        for relation in self.__relationships:
            res.write("\t" + relation.to_models_code() + "\n")
        return res.getvalue()


class AbstractRelationshipObject(ABC):
    """Represents JetUML's Association Edge"""

    def __init__(self):
        self.__source_class: Optional[ClassObject] = None
        self.__target_class: Optional[ClassObject] = None
        self.__sourceClassOwnAmount: str = ""
        self.__targetClassOwnAmount: str = ""

    def set_source_class(self, source_class: ClassObject):
        if source_class is None:
            raise Exception("Source Class cannot be SET to be None!")
        self.__source_class = source_class

    def set_target_class(self, target_class: ClassObject):
        if target_class is None:
            raise Exception("Target Class cannot be SET to be None!")
        self.__target_class = target_class

    def setSourceClassOwnAmount(self, amount: str):
        self.__sourceClassOwnAmount = amount

    def setTargetClassOwnAmount(self, amount: str):
        self.__targetClassOwnAmount = amount

    def get_source_class(self) -> ClassObject:
        return self.__source_class

    def get_target_class(self) -> ClassObject:
        return self.__target_class


class OneToOneRelationshipObject(AbstractRelationshipObject):
    """Represents JetUML's AssociationEdge where the the startLabel and endLabel are both '1'"""

    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()} = "
            + f"models.OneToOneField({self.get_target_class().get_name()},"
            + " on_delete = models.CASCADE)"
        )


class ManyToOneRelationshipObject(AbstractRelationshipObject):
    """
    Represents JetUML's AssociationEdge where one label is '*' and the other is '1'

    Note: Code generation is determined by the VALUES of startLabel and endLabel.
    Code generation must handle cases where startLabel is 1 and endLabel is *, and
    cases where startLabel is * and endLabel is *
    """

    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()}FK "
            + f"= models.ForeignKey({self.get_target_class().get_name()}, "
            + "on_delete = models.CASCADE)"
        )


class ManyToManyRelationshipObject(AbstractRelationshipObject):
    """Represents JetUML's AssociationEdge where both startLabel and endLabel are '*'"""

    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"listOf{self.get_target_class().get_name().title()}"
            + f" = models.ManyToManyField({self.get_target_class().get_name()},"
            + " on_delete = models.CASCADE)"
        )
