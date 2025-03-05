from __future__ import annotations

from abc import ABC
from typing import Optional

from app.utils import is_valid_python_identifier

from .methods import ClassMethodObject
from .properties import FieldObject


class ClassObject:
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
            + f"\n{self.__get_attributes_to_code()}\n{self.__get_relationships_to_code()}"
            + f"\n{self.__get_methods_to_code()}"
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

    def __get_attributes_to_code(self) -> str:
        res = ""
        for attribute in self.__fields:
            res += "\t" + attribute.to_models_code() + "\n"
        return res

    def __get_relationships_to_code(self) -> str:
        res = ""
        for relation in self.__relationships:
            res += "\t" + relation.to_models_code() + "\n"
        return res

    def __get_methods_to_code(self) -> str:
        # TODO: Implement this
        return ""


class AbstractRelationshipObject(ABC):
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
    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()} = "
            + f"models.OneToOneField({self.get_target_class().get_name()},"
            + " on_delete = models.CASCADE)"
        )


class ManyToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()}FK "
            + f"= models.ForeignKey({self.get_target_class().get_name()}, "
            + "on_delete = models.CASCADE)"
        )


class ManyToManyRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"listOf{self.get_target_class().get_name().title()}"
            + f" = models.ManyToManyField({self.get_target_class().get_name()},"
            + " on_delete = models.CASCADE)"
        )
