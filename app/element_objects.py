class ClassObject():

    def __init__(self):
        self.__name: str = ""
        self.__parent: ClassObject = None
        self.__fields : list[FieldObject] = []
        self.__methods : list[ClassMethodObject] = []
        self.__relationships : list[RelationshipObject] = []
        


    def __str__(self) -> str:
        pass
    def set_name(self, name):
        pass
    
    def set_parent(self, parent):
        pass

    def add_field(self, field):
        pass
    
    def add_method(self, method):
        pass

    def add_relationship(self, relationship):
        pass


class FieldObject():
    pass

class AbstractMethodObject():
    pass

class ClassMethodObject(AbstractMethodObject):
    pass

class RelationshipObject():
    pass

