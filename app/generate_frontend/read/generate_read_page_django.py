from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_html_read_pages_django(models_elements: ModelsElements) -> list[str]:
    if not isinstance(models_elements, ModelsElements):
        raise TypeError(
            f"Expected type ModelsElements, got {type(models_elements)} instead"
        )
    # Consider changing the code below to avoid memory explosion
    result = []
    for class_object in models_elements.get_classes():
        result.append(generate_html_read_page_django(class_object))
    return result


def generate_html_read_page_django(class_object: ClassObject) -> str:
    if not isinstance(class_object, ClassObject):
        raise TypeError(f"Expected type CLassObject, got {type(class_object)} instead")
    context = {
        "class_name": class_object.get_name(),
        "class_snake": camel_to_snake(class_object.get_name()),
    }
    fields = [{"name": f.get_name()} for f in class_object.get_fields()]
    context["fields"] = fields
    context["has_edit"] = len(fields) > 0
    return render_template("read_page_django.html.j2", context)
