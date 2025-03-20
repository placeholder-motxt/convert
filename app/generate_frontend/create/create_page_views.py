from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_create_page_views(models_elements: ModelsElements) -> str:
    classes = []
    if not models_elements.get_classes():
        raise ValueError("ModelsElements does not contain any classes!")
    for class_object in models_elements.get_classes():
        class_context = {
            "name": class_object.get_name(),
            "name_snake": camel_to_snake(class_object.get_name()),
        }
        classes.append(class_context)
    context = {"classes": classes}
    return render_template("create_page_views.py.j2", context)
