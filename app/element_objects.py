from abc import ABC, abstractmethod
from io import StringIO

class FileElements():
    def __init__(self, file_name : str):
        assert isinstance(file_name, str), "File name must be a string!"
        assert file_name != "", "File name can't be empty!"
        self.__name : str = file_name

class ModelsElements(FileElements):
    def __init__(self, file_name : str):
        super().__init__(file_name)
        self.__classes : list[ClassObject] = []

class ViewsElements(FileElements):
    def __init__(self, file_name : str):
        super().__init__(file_name)
        self.__class_methods : list[ClassMethodObject] = []
        self.__controller_methods : list[ControllerMethodObject] = []



class ClassObject():

    def __init__(self):
        self.__name: str = ""
        self.__parent: ClassObject = None
        self.__fields : list[FieldObject] = []
        self.__methods : list[ClassMethodObject] = []
        self.__relationships : list[AbstractRelationshipObject] = []
        


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


class AbstractMethodObject(ABC):
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

    def get_name(self):
        return self.__name
    
    def get_parameters(self):
        return self.__parameters


class ClassMethodObject(AbstractMethodObject):
    def __init__(self):
        super().__init__()
        self.__calls: list[ClassMethodCallObject] = []
    
    def add_class_method_call(self, class_method_call):
        if class_method_call == None:
            raise Exception("Cannot add None to ClassMethodCallObject!")
        self.__calls.append(class_method_call)

class AbstractRelationshipObject(ABC):
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

    def get_name(self):
        return self.__name

class AbstractMethodCallObject(ABC):
    def __init__(self):
        self.__method: AbstractMethodObject = None
        self.__arguments: list[ArgumentObject] = []
        self.__returnVarName: str = ""
        self.__condition = ""

    def __str__(self):
        return f'''MethodCallObject:\n\tmethod: {self.__method}\n\targuments: {self.__arguments}\n\treturnVarName: {self.__returnVarName}'''
    
    def set_method(self, method):
        self.__method = method

    def add_argument(self, argument):
        self.__arguments.append(argument)

    def set_returnVarName(self, returnVarName):
        self.__returnVarName = returnVarName

    def set_condition(self, condition):
        self.__condition = condition

    def print_django_style(self):
        result = StringIO()
        print("condition:", self.__condition)
        if self.__condition:
            print("ma2")
            result.write(f"if {self.__condition}:\n\t\t")
        if self.__returnVarName:
            result.write(f"{self.__returnVarName} = ")
        result.write(f"{self.__method.get_name()}(")
        if self.__arguments:
            arguments_str = ", ".join(arg.print_django_style() for arg in self.__arguments)
            result.write(arguments_str)
        result.write(")")
        return result.getvalue()
    
class ArgumentObject():
    def __init__(self):
        self.__methodObject: AbstractMethodCallObject = None
        self.__name: str = ""
        self.__type: TypeObject = None
    
    def __str__(self):
        return f'''ArgumentObject:\n\tmethodObject: \n\t[{self.__methodObject}]\n\tname: {self.__name}\n\ttype: \n\t[{self.__type}]'''
    
    def set_methodObject(self, methodObject):
        self.__methodObject = methodObject

    def set_name(self, name):
        self.__name = name

    def set_type(self, type):
        self.__type = type

    def print_django_style(self):
        return self.__name

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
        self.__caller : ClassMethodObject = None

    def set_caller(self, caller : ClassMethodObject):
        self.__caller = caller

class ControllerMethodObject(AbstractMethodObject):
    def __init__(self):
        super().__init__()
        self.__calls : list[AbstractMethodCallObject] = []
    
    def add_call(self, call_object : AbstractMethodCallObject):
        self.__calls.append(call_object)

    def print_django_style(self):
        if not self.get_name():
            raise TypeError("method cannot be empty")
        result = StringIO()
        result.write(f"def {self.get_name()}(request")
        for parameter in self.get_parameters():
            result.write(f", {parameter.get_name()}")
        result.write("):\n\t")
        for abstract_method_call_object in self.__calls:
            result.write(abstract_method_call_object.print_django_style())
            result.write("\n\t")
        result.write("\n")
        return result.getvalue()

class ClassMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None
    
    def set_caller(self, method_object):
        if method_object == None:
            raise Exception("ClassMethodObject cannot be SET to be None!")
        self.__caller = method_object