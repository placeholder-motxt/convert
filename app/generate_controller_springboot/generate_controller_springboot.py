from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.utils import logger, render_template, to_camel_case, to_pascal_case


def generate_springboot_controller_files(
    project_name: str, models_elements: ModelsElements, group_id: str
) -> list[str]:
    result = []
    for class_object in models_elements.get_classes():
        if class_object.get_is_public():
            result.append(
                generate_springboot_controller_file(
                    project_name, class_object, group_id
                )
            )
    return result


def generate_springboot_controller_file(
    project_name: str, class_object: ClassObject, group_id: str
) -> str:
    class_name = class_object.get_name()
    if not class_name:
        logger.error("Class name cannot be empty!")
        return ""
    context = {
        "class_pascal": to_pascal_case(class_name),
        "class_camel": to_camel_case(class_name),
        "project_name": project_name,
        "group_id": group_id,
        "is_public": class_object.get_is_public(),
    }
    try:
        return render_template("springboot_controller.java.j2", context)
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        return ""
