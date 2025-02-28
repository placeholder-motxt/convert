class ClassObject():

    def __init__(self):
        self.__name: str = ""
        self.__parent: ClassObject = None
        self.__fields : list[FieldObject] = []
        self.__methods : list[ClassMethodObject] = []
        self.__relationships : list[AbstractRelationshipObject] = []
        self.__id: int


    def __str__(self) -> str:
        return f'''Class Object:\n\tname: {self.__name}\n\tparent: {self.__parent}\n\tfields:{self.__fields}\n\t \
methods: {self.__methods}\n\trelationships: {self.__relationships}'''
    
    def to_models_code(self) -> str:
        return f"""class {self.__name}({self.__parent.get_name() if self.__parent else "models.Model"}):\n{self.__get_attributes_to_code()}\n{self.__get_relationships_to_code()}\n{self.__get_methods_to_code()}"""
    
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

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def __get_attributes_to_code(self):
        res=""
        for attribute in self.__fields:
            res+='\t'+attribute.to_models_code()+'\n'
        return res
    
    def __get_relationships_to_code(self):
        res=""
        for relation in self.__relationships:
            res+='\t'+relation.to_models_code()+'\n'
        return res
    
    def __get_methods_to_code(self):
        # TODO: Implement this
        return ""

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

    def to_models_code(self):
        type_mapping = {
        "boolean": "models.BooleanField()",
        "String": "models.CharField(max_length=255)",
        "integer": "models.IntegerField()",
        "float": "models.FloatField()",
        "double": "models.FloatField()",
        "Date": "models.DateField()",
        "DateTime": "models.DateTimeField()",
        "Time": "models.TimeField()",
        "Text": "models.TextField()",
        "Email": "models.EmailField()",
        "URL": "models.URLField()",
        "UUID": "models.UUIDField()",
        "Decimal": "models.DecimalField(max_digits=10, decimal_places=2)",
        }
    
        field_type = self.__type.to_models_code().lower()
        
        for key, value in type_mapping.items():
            if key.lower() in field_type:
                return f"{self.__name} = {value}"
        
        return f"{self.__name} = models.CharField(max_length=255)"  # Default fallback

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
    def __init__(self):
        super().__init__()
        self.__calls: list[ClassMethodCallObject] = []
    
    def add_class_method_call(self, class_method_call):
        if class_method_call == None:
            raise Exception("Cannot add None to ClassMethodCallObject!")
        self.__calls.append(class_method_call)

class AbstractRelationshipObject():
    def __init__(self):
        self.__sourceClass: ClassObject = None
        self.__targetClass: ClassObject = None
        self.__sourceClassOwnAmount: str = ""
        self.__targetClassOwnAmount: str = ""
    
    def setSourceClass(self, sourceClass):
        if sourceClass == None:
            raise Exception("Source Class cannot be SET to be None!")
        self.__sourceClass = sourceClass
    
    def setTargetClass(self, targetClass):
        if targetClass == None:
            raise Exception("Target Class cannot be SET to be None!")
        self.__targetClass = targetClass
    
    def setSourceClassOwnAmount(self, amount):
        self.__sourceClassOwnAmount = amount

    def setTargetClassOwnAmount(self, amount):
        self.__targetClassOwnAmount = amount

    def get_source_class(self):
        return self.__sourceClass
    
    def get_target_class(self):
        return self.__targetClass

class TypeObject():
    def __init__(self):
        self.__name = ""
    
    def set_name(self, name):
        self.__name = name
    
    def to_models_code(self):
        return self.__name.title()

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

class AbstractMethodCallObject():
    def __init__(self):
        self.__method: AbstractMethodObject = None
        self.__arguments: list[ArgumentObject] = []
        self.__returnVarName: str = ""

    def __str__(self):
        return f'''MethodCallObject:\n\tmethod: {self.__method}\n\targuments: {self.__arguments}\n\treturnVarName: {self.__returnVarName}'''
    
    def set_method(self, method):
        self.__method = method

    def add_argument(self, argument):
        self.__arguments.append(argument)

    def set_returnVarName(self, returnVarName):
        self.__returnVarName = returnVarName

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

class OneToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()
    
    def to_models_code(self):
        return f"{self.get_target_class().get_name().lower()} = models.OneToOneField({self.get_target_class().get_name()}, on_delete = models.CASCADE)"

class ManyToOneRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()

    def to_models_code(self):
        return f"{self.get_target_class().get_name().lower()}FK = models.ForeignKey({self.get_target_class().get_name()}, on_delete = models.CASCADE)"

class ManyToManyRelationshipObject(AbstractRelationshipObject):
    def __init__(self):
        super().__init__()
    
    def to_models_code(self):
        return f"listOf{self.get_target_class().get_name().title()} = models.ManyToManyField({self.get_target_class().get_name()}, on_delete = models.CASCADE)"


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
    
    def add_calls(self, call_object : AbstractMethodCallObject):
        self.__calls.append(call_object)

class ClassMethodCallObject(AbstractMethodCallObject):
    def __init__(self):
        super().__init__()
        self.__caller: ClassMethodObject = None
    
    def set_caller(self, method_object):
        if method_object == None:
            raise Exception("ClassMethodObject cannot be SET to be None!")
        self.__caller = method_object