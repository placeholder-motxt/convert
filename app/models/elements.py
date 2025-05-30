import logging
from abc import ABC, abstractmethod
from io import StringIO

import anyio

from app.parse_json_to_object_class import ParseJsonToObjectClass
from app.utils import camel_to_snake, render_template

from .diagram import ClassObject
from .methods import ClassMethodObject, ControllerMethodObject

logger = logging.getLogger("uvicorn.error")


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

    async def write_to_file(self, path: str) -> None:
        file = path + "/" + self.__name
        to_be_print = self.print_django_style()

        async with await anyio.open_file(file, "w") as f:
            await f.write(to_be_print)
        print("done writing", file)
        return file


class ModelsElements(FileElements):
    """An intermediate representation of information inside a models file

    Note: this class is NOT FRAMEWORK SPECIFIC
    """

    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.__classes: list[ClassObject] = []

    def get_classes(self) -> list[ClassObject]:  # pragma: no cover
        return self.__classes

    def add_class(self, class_object: ClassObject):
        if not isinstance(class_object, ClassObject):
            raise ValueError(
                "only ClassObjects can be added to ModelsElements' Class Field!"
            )
        self.__classes.append(class_object)

    """
    Parses ClassDiagram to classes
    """

    def parse(self, content: str, bidirectional: bool = False) -> list[ClassObject]:
        parser = ParseJsonToObjectClass(content)
        self.__classes = parser.parse_classes()
        parser.parse_relationships(self.__classes, bidirectional)
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

    def print_django_style_template(self, template_name: str = "models.py.j2") -> str:
        try:
            return render_template(
                template_name,
                {
                    "classes": [
                        model_class.to_models_code_template_context()
                        for model_class in self.__classes
                    ]
                },
            )
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return ""

    def print_springboot_style(
        self, project_name: str, group_id: str
    ) -> dict[str, str]:
        """
        Returns a dictionary containing the class name as the key and
        the rendered model files as the value

        Example:

        {
            "Class1": "Rendered Jinja template for Class1",
            "Class2": "Rendered Jinja template for Class2",
            ...
        }

        """
        try:
            files = {}
            for model_class in self.__classes:
                ctx = model_class.to_models_springboot_context()
                ctx["project_name"] = project_name
                ctx["group_id"] = group_id

                files[model_class.get_name()] = render_template(
                    "springboot/model.j2", context=ctx
                )
            return files
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return {}


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

    def print_django_style_template(self) -> str:
        context = {}
        class_method_context = [
            class_method_object.to_views_code_template()
            for class_method_object in self.__class_methods
        ]
        controller_method_context = [
            controller_method_object.print_django_style_template()
            for controller_method_object in self.__controller_methods
        ]

        context["class_methods"] = class_method_context
        context["controller_methods"] = controller_method_context

        try:
            return render_template("sequence_views.py.j2", context)
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return ""


class UrlsElement(FileElements):
    def __init__(self, file_name: str = "urls.py"):
        super().__init__(file_name)
        self.__classes: list[ClassObject] = []

    def set_classes(self, classes: list[ClassObject]) -> None:  # pragma: no cover
        self.__classes = classes

    def print_django_style(self) -> str:
        classes = []
        for kelas in self.__classes:
            class_context = {
                "name": kelas.get_name(),
                "snake_name": camel_to_snake(kelas.get_name()),
                "is_public": kelas.get_is_public(),
            }
            classes.append(class_context)
        return render_template("urls.py.j2", classes=classes)


class RequirementsElements(FileElements):
    def __init__(self, file_name: str = "requirements.txt"):
        """
        Object initialization

        This class is only for writing requirements.txt,
        """
        super().__init__(file_name)

    def print_django_style(self) -> str:
        """
        Returns a list of django requirements as string for requirements.tx to run
        """
        result = StringIO()
        requirements = [
            "Django",
            "gunicorn",
            "whitenoise",
            "psycopg2-binary",
            "pytest",
            "pytest-django",
            "pytest-cov",
        ]

        for requirement in requirements:
            result.write(requirement + "\n")

        return result.getvalue()


class RunBashScriptElements(FileElements):
    """
    This class is only for writing script for user to run the project in format
    of .sh (Linux & MacOS)
    """

    def print_django_style(self) -> str:
        with open("app/templates/scripts/run.sh.txt", "r", encoding="utf-8") as file:
            bash = file.read()
        return bash


class RunBatScriptElements(FileElements):
    """
    This class is only for writing script for user to run the project in format
    of .bat (Windows)
    """

    def print_django_style(self) -> str:
        with open("app/templates/scripts/run.bat.txt", "r", encoding="utf-8") as file:
            bat = file.read()
        return bat


class DependencyElements(FileElements):
    """
    This class is only for writing script for dependency in springboot framework
    """

    def print_django_style(self) -> str:  # pragma: no cover
        """
        Only for abstract method purposes and doesn't return anything
        """
        return super().print_django_style()

    def print_application_properties(self) -> str:
        config = {
            "springdoc.api-docs.enabled": "true",
            "springdoc.swagger-ui.enabled": "true",
            "spring.datasource.url": "jdbc:sqlite:mydatabase.db",
            "spring.datasource.driver-class-name": "org.sqlite.JDBC",
            "spring.jpa.show-sql": "true",
            "spring.jpa.database-platform": "org.hibernate.community.dialect.SQLiteDialect",
            "spring.jpa.hibernate.ddl-auto": "update",
        }
        return "\n".join(f"{key}={value}" for key, value in config.items()) + "\n"

    def print_springboot_style(self, project_name: str) -> str:
        context = {
            "project_name": project_name,
            "java": "21",
            "spring_boot": "3.4",
            "dependencies": [
                "org.springframework.boot:spring-boot-starter-thymeleaf",
                "org.springframework.boot:spring-boot-starter-web",
                "org.springframework.boot:spring-boot-starter-data-jpa",
                "org.springframework.boot:spring-boot-starter-validation",
                "org.springframework.boot:spring-boot-starter",
                "com.zaxxer:HikariCP",
                "org.xerial:sqlite-jdbc:3.41.2.2",
                "jakarta.persistence:jakarta.persistence-api:3.1.0",
                "org.springdoc:springdoc-openapi-starter-webmvc-ui:2.2.0",
                "org.hibernate:hibernate-core:5.6.9.Final",
                "org.xerial:sqlite-jdbc:3.41.2.2",
                "org.hibernate.orm:hibernate-community-dialects",
            ],
            "repositories": [
                "mavenCentral()",
                "maven { url 'https://repo.spring.io/milestone' }",
                "maven { url 'https://repo.spring.io/release' }",
            ],
        }
        try:
            if project_name == "":
                raise ValueError("Project name cannot be empty!")
            return render_template("springboot/build.gradle.kts.j2", context=context)
        except Exception as e:
            raise ValueError(f"Error rendering template: {e}")
