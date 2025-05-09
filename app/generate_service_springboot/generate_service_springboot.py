import re

from app.models.diagram import ClassObject
from app.utils import render_template


def generate_service_java(project_name: str, model: ClassObject, group_id: str) -> str:
    """
    This method is used to generate Service.java for single ClassObject

    Example: If the ClassObject name is Cart, then it will generate
    CartService.java

    In the main.py, you need to loop for each ClassObject and call the
    generate_service_java to create separate service based on the Class
    """
    class_name_capital, class_name = format_class_name(model.get_name())
    method = []

    for methods in model.get_methods():
        method.append(methods.to_springboot_code())

    context = {
        "project_name": project_name,
        "class_name_capital": class_name_capital,
        "class_name": class_name,
        "is_public": model.get_is_public(),
        "attributes": get_all_attributes(model),
        "method": method,
        "group_id": group_id,
    }
    return render_template("springboot/service.java.j2", context)


def get_all_attributes(model: ClassObject) -> list[str]:
    attributes = []

    fields = []
    fields += model.get_fields()

    parent = model.get_parent()

    while parent is not None:
        fields += parent.get_fields()
        parent = parent.get_parent()

    for attribute in fields:
        attribute_name = attribute.get_name()
        name = attribute_name[0].upper() + attribute_name[1:]

        if (
            attribute.get_type() == "boolean" or attribute.get_type() == "bool"
        ) and bool(re.match(r"^is[A-Z].*", attribute_name)):
            getter = attribute.get_name()
            setter = "set" + attribute.get_name()[2:]
        else:
            getter = "get" + attribute_name[0].upper() + attribute_name[1:]
            setter = "set" + attribute_name[0].upper() + attribute_name[1:]
        attributes.append((name, getter, setter))

    return attributes


def format_class_name(name: str) -> tuple[str, str]:
    return name.capitalize(), name[0].lower() + name[1:]
