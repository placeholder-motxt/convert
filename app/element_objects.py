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
    pass

class AbstractMethodObject():
    pass

class ClassMethodObject(AbstractMethodObject):
    pass

class RelationshipObject():
    pass

