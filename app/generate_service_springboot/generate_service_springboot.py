import re

from app.models.diagram import ClassObject
from app.models.elements import ViewsElements
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

    attributes = []
    for attribute in model.get_fields():
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

    context = {
        "project_name": project_name,
        "class_name_capital": class_name_capital,
        "class_name": class_name,
        "is_public": model.get_is_public(),
        "attributes": attributes,
        "method": method,
        "group_id": group_id,
    }
    return render_template("springboot/service.java.j2", context)


def format_class_name(name: str) -> tuple[str, str]:
    return name.capitalize(), name[0].lower() + name[1:]


def generate_sequence_service_java(
    project_name: str, views_elements: ViewsElements, group_id: str
) -> str:
    context = {"project_name": project_name, "group_id": group_id}
    if len(views_elements.get_controller_methods()) == 0:
        return ""
    controller_method_context = [
        controller_method_object.print_springboot_style_template()
        for controller_method_object in views_elements.get_controller_methods()
    ]
    context["controller_methods"] = controller_method_context
    return render_template("SequenceService.java.j2", context)
