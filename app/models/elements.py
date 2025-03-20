from abc import ABC, abstractmethod
from io import StringIO

from app.parse_json_to_object_class import ParseJsonToObjectClass

from .diagram import ClassObject
from .methods import ClassMethodObject, ControllerMethodObject


class FileElements(ABC):
    """
    An intermediate representation of information that will be generated into one file

    It is not a representation of JetUML files, rather it is a representation of
    to-be-generated files.
    This class contains abstract methods to write the contents of the class into a file
    according to the chosen framework. Currently the only available framework is Django


    """

    def __init__(self, file_name: str):
        if not isinstance(file_name, str):
            raise TypeError("File name must be a string!")
        if file_name == "":
            raise ValueError("File name can't be empty!")
        self.__name: str = file_name

    @abstractmethod
    def print_django_style(self) -> str:  # pragma: no cover
        pass


class ModelsElements(FileElements):
    """An intermediate representation of information inside a models file

    Note: this class is NOT FRAMEWORK SPECIFIC
    """

    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__classes: list[ClassObject] = []


    def get_classes(self) -> list[ClassObject]: # pragma: no cover
        return self.__classes

    def add_class(self, class_object: ClassObject):
        if not isinstance(class_object, ClassObject):
            raise ValueError("only ClassObjects can be added to ModelsElements' Class Field!")
        self.__classes.append(class_object)


    """
    Parses ClassDiagram to classes
    """

    def parse(self, content: str) -> list[ClassObject]:
        parser = ParseJsonToObjectClass(content)
        self.__classes = parser.parse_classes()
        parser.parse_relationships(self.__classes)
        return self.__classes

    """
    Writes classes to models.py
    """

    def print_django_style(self) -> str:
        # A faster way to build string
        # https://stackoverflow.com/questions/2414667/python-string-class-like-stringbuilder-in-c
        response_content = "from django.db import models\n\n"
        response_content += "".join(
            [model_class.to_models_code() for model_class in self.__classes]
        )
        response_content = response_content.strip()
        response_content += "\n" if len(response_content) != 0 else ""
        return response_content


class ViewsElements(FileElements):
    """
    An intermediate representation of information inside a views file

    A views file is a file that contains the business logic of the web application.
    The file name may differ across different frameworks.
    """

    def __init__(self, file_name: str):
        """
        Object initialization

        This class may contain both ClassMethodObjects and ControllerMethodObjects,
        """
        super().__init__(file_name)
        self.__class_methods: list[ClassMethodObject] = []
        self.__controller_methods: list[ControllerMethodObject] = []

    def print_django_style(self) -> str:
        """
        Returns Django's views.py code in string, representing the contents of the class

        Example:
        ViewsElements object contains two ClassMethodObject objects and one ControllerMethodObject
        object, with class names Class1 and Class2 respectively, and with method names
        class_method_1, class_method_2, and controller_method_1 respectively. The output of the
        method will be as follows:

        #-----method from class Class1------

        def class_method_1(request, ....):
            ...
            ...


        #-----method from class Class2------

        def class_method_2(request, ....):
            ...
            ...


        def controller_method_1(request, ...):
            ...
            ...
        """
        result = StringIO()

        for class_method_object in self.__class_methods:
            result.write(
                f"#-----method from class {class_method_object.get_name()}------\n\n"
            )
            result.write(class_method_object.to_views_code())
            result.write("\n\n\n")

        for controller_method_object in self.__controller_methods:
            result.write(controller_method_object.print_django_style())
        return result.getvalue()

    def add_class_method(self, class_method_object: ClassMethodObject):
        self.__class_methods.append(class_method_object)

    def add_controller_method(self, controller_method_object: ControllerMethodObject):
        self.__controller_methods.append(controller_method_object)

