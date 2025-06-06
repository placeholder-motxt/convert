from __future__ import annotations

from abc import ABC
from io import StringIO
from typing import Optional

from app.utils import is_valid_python_identifier, to_camel_case, to_pascal_case

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
        self.__is_public: bool = False

        self.__id: int

    def get_fields(self) -> list[FieldObject]:  # pragma: no cover
        return self.__fields

    def get_parent(self) -> ClassObject:  # pragma: no cover
        return self.__parent

    def to_models_code(self) -> str:
        return (
            f"class {self.__name}"
            + f"({self.__parent.get_name() if self.__parent else 'models.Model'}):"
            + f"\n{self.__get_attributes_to_code()}\n"
            + f"{self.__get_relationships_to_code()}\tpass\n\n\n"
        )

    def to_views_code(self) -> str:
        if not is_valid_python_identifier(self.__name):
            raise ValueError(
                f"Invalid class name '{self.__name}'\n"
                "please consult the user manual document on how to name classes"
            )

        res = ""
        if len(self.__methods) > 0:
            res = f"from .models import {self.__name}\n"

        if self.__parent is not None:
            res += self.__parent.to_views_code()

        for method in self.__methods:
            res += method.to_views_code()

        return res

    def to_models_code_template_context(self) -> dict[str]:
        ctx = {
            "name": self.get_name(),
            "parent": self.__parent.get_name() if self.__parent else "models.Model",
            "fields": [],
        }

        for field in self.__fields:
            ctx["fields"].append(field.to_models_code_template())

        for relationship in self.__relationships:
            ctx["fields"].append(relationship.to_models_code_template())

        return ctx

    def to_models_springboot_context(self) -> dict[str, dict[str]]:
        """Returns a dictionary with the class name, parent class name, fields and relationships
        for the Spring Boot template."""
        ctx = {
            "name": to_pascal_case(self.get_name()),
            "parent": to_pascal_case(self.__parent.get_name())
            if self.__parent
            else None,
            "fields": [],
            "relationships": [],
        }

        for field in self.__fields:
            ctx["fields"].append(field.to_springboot_models_template())

        for relationship in self.__relationships:
            ctx["relationships"].append(relationship.to_springboot_models_template())

        return ctx

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

    def set_is_public(self, is_public: bool):
        self.__is_public = is_public

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

    def get_is_public(self) -> bool:
        return self.__is_public


class AbstractRelationshipObject(ABC):
    """Represents JetUML's Association Edge"""

    def __init__(self):
        self.__source_class: Optional[ClassObject] = None
        self.__target_class: Optional[ClassObject] = None
        self.__sourceClassOwnAmount: str = ""
        self.__targetClassOwnAmount: str = ""

    def set_source_class(self, source_class: ClassObject):
        if source_class is None:
            raise ValueError(
                "Source Class cannot be SET to be None!\n "
                "Relationship in class diagram is wrong"
            )
        self.__source_class = source_class

    def set_target_class(self, target_class: ClassObject):
        if target_class is None:
            raise ValueError(
                "Target Class cannot be SET to be None!\n "
                "Relationship in class diagram is wrong"
            )
        self.__target_class = target_class

    def set_source_class_own_amount(self, amount: str):
        self.__sourceClassOwnAmount = amount

    def set_target_class_own_amount(self, amount: str):
        self.__targetClassOwnAmount = amount

    def get_source_class(self) -> ClassObject:
        return self.__source_class

    def get_target_class(self) -> ClassObject:
        return self.__target_class

    def get_source_class_own_amount(self) -> str:  # pragma: no cover
        return self.__sourceClassOwnAmount

    def get_target_class_own_amount(self) -> str:  # pragma: no cover
        return self.__targetClassOwnAmount


class OneToOneRelationshipObject(AbstractRelationshipObject):
    """Represents JetUML's AssociationEdge where the the startLabel and endLabel are both '1'"""

    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"{self.get_target_class().get_name().lower()} = "
            + f"models.OneToOneField('{self.get_target_class().get_name()}',"
            + " on_delete = models.CASCADE)"
        )

    def to_models_code_template(self) -> dict[str, str]:
        name = self.get_target_class().get_name()
        rel_type = f"models.OneToOneField('{name}', on_delete=models.CASCADE)"
        return {"name": name.lower(), "type": rel_type}

    def to_springboot_models_template(self) -> dict[str, str]:
        source = self.get_source_class().get_name().lower()
        target = self.get_target_class().get_name()
        if self.get_source_class_own_amount() != "1+":
            rel_type = f'@OneToOne(mappedBy="{source.replace(" ", "_")}")'
            join = None
        else:
            rel_type = (
                "@OneToOne(cascade = {CascadeType.PERSIST, CascadeType.MERGE, "
                "CascadeType.REMOVE})"
            )
            join = f'@JoinColumn(name = "{source.replace(" ", "_")}_id")'
        var = f"private {to_pascal_case(target)} {to_camel_case(target)};"
        return {"name": var, "type": rel_type, "join": join}


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
            + f"= models.ForeignKey('{self.get_target_class().get_name()}', "
            + "on_delete = models.CASCADE)"
        )

    def to_models_code_template(self) -> dict[str, str]:
        name = self.get_target_class().get_name()
        rel_type = f"models.ForeignKey('{name}', on_delete=models.CASCADE)"
        return {"name": f"{name.lower()}FK", "type": rel_type}

    def to_springboot_models_template(self) -> dict[str, str]:
        source = self.get_source_class().get_name().lower()
        target = self.get_target_class().get_name()
        if self.get_source_class_own_amount() == "1":
            rel_type = f'@ManyToOne(mappedBy="{source.replace(" ", "_")}_id")'
            rel_type += f'\n\t@JsonIgnoreProperties("{source.replace(" ", "_")}s")'
            join = None
            var = f"private {to_pascal_case(target)} {to_camel_case(target)};"
        else:
            rel_type = (
                "@OneToMany(\n\t\tcascade = {CascadeType.PERSIST, CascadeType.MERGE},"
            )
            rel_type += "\n\t\torphanRemoval = true\n)"
            rel_type += "\n\t@JsonIgnore"
            join = f'@JoinColumn(name = "{source.replace(" ", "_")}_id")'
            var = f"private List<{to_pascal_case(target)}> {to_camel_case(target)}s;"
        return {"name": var, "type": rel_type, "join": join}


class ManyToManyRelationshipObject(AbstractRelationshipObject):
    """Represents JetUML's AssociationEdge where both startLabel and endLabel are '*'"""

    def __init__(self):
        super().__init__()

    def to_models_code(self) -> str:
        return (
            f"listOf{self.get_target_class().get_name().title()}"
            + f" = models.ManyToManyField('{self.get_target_class().get_name()}'"
            + ")"
        )

    def to_models_code_template(self) -> dict[str, str]:
        name = self.get_target_class().get_name()
        rel_type = f"models.ManyToManyField('{name}')"
        return {"name": f"listOf{name.title()}", "type": rel_type}

    def to_springboot_models_template(self) -> dict[str, str]:
        source = self.get_source_class().get_name().lower()
        target = self.get_target_class().get_name()
        rel_type = "@ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})"
        rel_type += "\n\t@JsonIgnore"
        join = "@JoinTable("
        join += f'\n\t\tname = "{source.replace(" ", "_")}_{target.replace(" ", "_").lower()}",'
        join += (
            f'\n\t\tjoinColumns = @JoinColumn(name = "{source.replace(" ", "_")}_id"),'
        )
        join += (
            f"\n\t\tinverseJoinColumns = @JoinColumn("
            f'name = "{target.replace(" ", "_").lower()}_id")\n\t)'
        )
        var = f"private List<{to_pascal_case(target)}> listOf{to_pascal_case(target)}s;"
        return {"name": var, "type": rel_type, "join": join}
