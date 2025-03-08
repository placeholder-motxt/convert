from abc import ABC, abstractmethod
from io import StringIO

from .diagram import ClassObject
from .methods import ClassMethodObject, ControllerMethodObject


class FileElements(ABC):
    def __init__(self, file_name: str):
        assert isinstance(file_name, str), "File name must be a string!"
        assert file_name != "", "File name can't be empty!"
        self.__name: str = file_name

    @abstractmethod
    def print_django_style(self) -> str:  # pragma: no cover
        pass


class ModelsElements(FileElements):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__classes: list[ClassObject] = []

    def print_django_style(self) -> str:
        pass  # TODO: PBI 1-7



class ViewsElements(FileElements):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__class_methods: list[ClassMethodObject] = []
        self.__controller_methods: list[ControllerMethodObject] = []

    def print_django_style(self) -> str:
        result = StringIO()

        for class_method_object in self.__class_methods:
            result.write(f"#-----method from class {class_method_object.get_name()}------\n\n")
            result.write(class_method_object.print_django_style())
            result.write("\n\n\n")

        for controller_method_object in self.__controller_methods:
            result.write(controller_method_object.print_django_style())
        return result.getvalue()

    def add_class_method(self, class_method_object: ClassMethodObject):
        self.__class_methods.append(class_method_object)

    def add_controller_method(self, controller_method_object: ControllerMethodObject):
        self.__controller_methods.append(controller_method_object)

