from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.utils import render_template


def generate_html_create_pages_django(models_elements: ModelsElements) -> list[str]:
    result = []
    for class_object in models_elements.get_classes():
        if class_object.get_is_public():
            result.append(generate_html_create_page_django(class_object))
    return result


def generate_html_create_page_django(class_object: ClassObject) -> str:
    context = {"class_name": class_object.get_name()}
    return render_template("create_page_django.html.j2", context)


def generate_forms_create_page_django(models_elements: ModelsElements) -> str:
    classes = []
    for class_object in models_elements.get_classes():
        if class_object.get_is_public():
            class_context = {
                "name": class_object.get_name(),
                "fields": [
                    {"name": field.get_name()} for field in class_object.get_fields()
                ],
            }
            classes.append(class_context)
    context = {"classes": classes}
    return render_template("forms.py.j2", context)
