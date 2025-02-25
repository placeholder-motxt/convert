class ClassObject():

    def __init__(self):
        self.__name: str = ""
        self.__parent: ClassObject = None
        self.__fields : list[FieldObject] = []
        self.__methods : list[ClassMethodObject] = []
        self.__relationships : list[RelationshipObject] = []
        


    def __str__(self) -> str:
        return f'''Class Object:\n\tname: {self.__name}\n\tparent: {self.__parent}\n\tfields:{self.__fields}\n\t \
methods: {self.__methods}\n\trelationships: {self.__relationships}'''
    
    def set_name(self, name):
        self.__name = name
    
    def set_parent(self, parent):
        self.__parent = parent

    def add_field(self, field):
        self.__fields.append(field)
    
    def add_method(self, method):
        self.__methods.append(method)

    def add_relationship(self, relationship):
        self.__relationships.append(relationship)


class FieldObject():
    
    def __init__(self):
        self.__name : str = ""
        self.__type : TypeObject = None

    def __str__(self):
        return f'''FieldObject:\n\tname: {self.__name}\n\ttype: {self.__type}'''
    
    def set_name(self, name):
        self.__name = name
    
    def set_type(self, type):
        self.__type = type


class AbstractMethodObject():
    def __init__(self):
        self.__name : str = ""
        self.__parameters : list[ParameterObject] = []
        self.__returnType : TypeObject = None

    def __str__(self):
        return f'''MethodObject:\n\tname: {self.__name}\n\tparameters: {self.__parameters}\n\treturnType: {self.__returnType}'''
    
    def set_name(self, name):
        self.__name = name

    def add_parameter(self, parameter):
        self.__parameters.append(parameter)

    def set_returnType(self, returnType):
        self.__returnType = returnType


class ClassMethodObject(AbstractMethodObject):
    pass

class RelationshipObject():
    def __init__(self):
        self.__sourceClass: ClassObject = None
        self.__targetClass: ClassObject = None
    
    def setSourceClass(self, sourceClass):
        if sourceClass == None:
            raise Exception("Source Class cannot be SET to be None!")
        self.__sourceClass = sourceClass
    
    def setTargetClass(self, targetClass):
        if targetClass == None:
            raise Exception("Target Class cannot be SET to be None!")
        self.__targetClass = targetClass

class TypeObject():
    def __init__(self):
        self.__name = ""
    
    def set_name(self, name):
        self.__name = name
        

class ParameterObject():
    def __init__(self):
        self.__name: str = ""
        self.__type: TypeObject = None

    def __str__(self):
        return f'''ParameterObject:\n\tname: {self.__name}\n\ttype: {self.__type}'''
    
    def set_name(self, name):
        self.__name = name
    
    def set_type(self, type):
        self.__type = type      