from __future__ import annotations


class ClassObject:
    def __init__(self):
        self.__name: str = ""
        self.__parent: ClassObject = None
        self.__fields: list[FieldObject] = []
        self.__methods: list[ClassMethodObject] = []
        self.__relationships: list[AbstractRelationshipObject] = []

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


class FieldObject:
    def __init__(self):
        self.__name: str = ""
        self.__type: TypeObject = None

    def __str__(self) -> str:
        return f"""FieldObject:\n\tname: {self.__name}\n\ttype: {self.__type}"""

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: TypeObject):
        self.__type = type


class AbstractMethodObject:
    def __init__(self):
        self.__name: str = ""
        self.__parameters: list[ParameterObject] = []
        self.__returnType: TypeObject = None

    def __str__(self) -> str:
        return (
            f"MethodObject:\n\tname: {self.__name}\n\tparameters: {self.__parameters}"
            f"\n\treturnType: {self.__returnType}"
        )

    def set_name(self, name: str):
        self.__name = name

    def add_parameter(self, parameter: ParameterObject):
        self.__parameters.append(parameter)

    def set_returnType(self, returnType: TypeObject):
        self.__returnType = returnType


class ClassMethodObject(AbstractMethodObject):
    def __init__(self):
        super().__init__()
        self.__calls: list[ClassMethodCallObject] = []

    def add_class_method_call(self, class_method_call: ClassMethodCallObject):
        if class_method_call is None:
            raise Exception("Cannot add None to ClassMethodCallObject!")
        self.__calls.append(class_method_call)


class AbstractRelationshipObject:
    def __init__(self):
        self.__sourceClass: ClassObject = None
        self.__targetClass: ClassObject = None

    def setSourceClass(self, sourceClass: ClassObject):
        if sourceClass is None:
            raise Exception("Source Class cannot be SET to be None!")
        self.__sourceClass = sourceClass

    def setTargetClass(self, targetClass: ClassObject):
        if targetClass is None:
            raise Exception("Target Class cannot be SET to be None!")
        self.__targetClass = targetClass


class TypeObject:
    def __init__(self):
        self.__name = ""

    def set_name(self, name: str):
        self.__name = name


class ParameterObject:
    def __init__(self):
        self.__name: str = ""
        self.__type: TypeObject = None

    def __str__(self) -> str:
        return f"""ParameterObject:\n\tname: {self.__name}\n\ttype: {self.__type}"""

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: str):
        self.__type = type


class AbstractMethodCallObject:
    def __init__(self):
        self.__method: AbstractMethodObject = None
        self.__arguments: list[ArgumentObject] = []
        self.__returnVarName: str = ""

    def __str__(self) -> str:
        return (
            f"MethodCallObject:\n\tmethod: {self.__method}\n\t"
            f"arguments: {self.__arguments}\n\treturnVarName: {self.__returnVarName}"
        )

    def set_method(self, method: AbstractMethodObject):
        self.__method = method

    def add_argument(self, argument: ArgumentObject):
        self.__arguments.append(argument)

    def set_returnVarName(self, returnVarName: str):
        self.__returnVarName = returnVarName


class ArgumentObject:
    def __init__(self):
        self.__methodObject: AbstractMethodCallObject = None
        self.__name: str = ""
        self.__type: TypeObject = None

    def __str__(self) -> str:
        return (
            f"ArgumentObject:\n\tmethodObject: \n\t[{self.__methodObject}]"
            f"\n\tname: {self.__name}\n\ttype: \n\t[{self.__type}]"
        )

    def set_methodObject(self, methodObject: AbstractMethodCallObject):
        self.__methodObject = methodObject

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, type: TypeObject):
        self.__type = type


class OneToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()


class ManyToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()


class ManyToManyRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()


class ControllerMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None

    def set_caller(self, caller: ClassMethodObject):
        self.__caller = caller


class ControllerMethodObject(AbstractMethodObject):
    def __init__(self):
        super().__init__()
        self.__calls: list[AbstractMethodCallObject] = []

    def add_calls(self, call_object: AbstractMethodCallObject):
        self.__calls.append(call_object)


class ClassMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None

    def set_caller(self, method_object: ClassMethodObject):
        if method_object is None:
            raise Exception("ClassMethodObject cannot be SET to be None!")
        self.__caller = method_object
