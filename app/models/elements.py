from abc import ABC, abstractmethod
from io import StringIO

from app.parse_json_to_object_class import ParseJsonToObjectClass

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

    def parse(self, content: str) -> list[ClassObject]:
        """
        Parses ClassDiagram to classes
        """
        parser = ParseJsonToObjectClass(content)
        self.__classes = parser.parse_classes()
        parser.parse_relationships(self.__classes)
        return self.__classes

    def print_django_style(self) -> str:
        # A faster way to build string
        # https://stackoverflow.com/questions/2414667/python-string-class-like-stringbuilder-in-c
        response_content = "".join(
            [model_class.to_models_code() for model_class in self.__classes]
        )
        response_content = response_content.strip()
        response_content += "\n" if len(response_content) != 0 else ""
        return response_content


class ViewsElements(FileElements):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__class_methods: list[ClassMethodObject] = []
        self.__controller_methods: list[ControllerMethodObject] = []

    def print_django_style(self) -> str:
        result = StringIO()

        for class_method_object in self.__class_methods:
            result.write(class_method_object.to_views_code())
            # TODO: PBI-1-7
            # TODO: PBI 2-9
            pass

        for controller_method_object in self.__controller_methods:
            result.write(controller_method_object.print_django_style())
        return result.getvalue()

    def add_class_method(self, class_method_object: ClassMethodObject):
        self.__class_methods.append(class_method_object)

    def add_controller_method(self, controller_method_object: ControllerMethodObject):
        self.__controller_methods.append(controller_method_object)
