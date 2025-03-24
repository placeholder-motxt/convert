from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_html_read_pages_django(models_elements: ModelsElements) -> list[str]:
    if not isinstance(models_elements, ModelsElements):
        raise (TypeError("argument must be of type ModelsElements!"))
    result = []
    for class_object in models_elements.get_classes():
        result.append(generate_html_read_page_django(class_object))
    return result


def generate_html_read_page_django(class_object: ClassObject) -> str:
    if not isinstance(class_object, ClassObject):
        raise (TypeError("argument must be of type ClassObject!"))
    context = {
        "class_name": class_object.get_name(),
        "class_snake": camel_to_snake(class_object.get_name()),
    }
    fields = []
    for field in class_object.get_fields():
        fields.append({"name": field.get_name()})
    context["fields"] = fields
    return render_template("read_page_django.html.j2", context)
