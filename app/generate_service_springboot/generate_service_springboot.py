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

    attributes = []
    for attribute in model.get_fields():
        attribute_name = attribute.get_name()
        attributes.append(attribute_name[0].upper() + attribute_name[1:])

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
