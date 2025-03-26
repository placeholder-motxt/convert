from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_edit_page_views(models_elements: ModelsElements) -> str:
    class_objects = models_elements.get_classes()
    if len(class_objects) == 0:
        raise ValueError("Can't create edit views with no class")

    classes = []
    for class_object in class_objects:
        if len(class_object.get_fields()) == 0:
            continue
        class_context = {
            "name": class_object.get_name(),
            "snake_name": camel_to_snake(class_object.get_name()),
        }
        classes.append(class_context)
    context = {"classes": classes}
    return render_template("edit_page_views.py.j2", context)
