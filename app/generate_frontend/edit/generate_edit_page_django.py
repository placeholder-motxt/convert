from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.utils import render_template


def generate_html_edit_pages_django(models_elements: ModelsElements) -> list[str]:
    result = []
    for class_object in models_elements.get_classes():
        if class_object.get_name() == "" or len(class_object.get_fields()) == 0:
            continue

        result.append(generate_html_edit_page_django(class_object))
    return result


def generate_html_edit_page_django(class_object: ClassObject) -> str:
    if class_object.get_name() == "" or len(class_object.get_fields()) == 0:
        return ""

    context = {"class_name": class_object.get_name()}
    return render_template("edit_page_django.html.j2", context)
