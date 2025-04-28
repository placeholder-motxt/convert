from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_create_page_views(models_elements: ModelsElements) -> str:
    classes = []
    if not models_elements.get_classes():
        raise ValueError("ModelsElements does not contain any classes!")
    for class_object in models_elements.get_classes():
        if class_object.get_is_public():
            cls_name = class_object.get_name()
            class_context = {
                "name": cls_name,
                "name_snake": camel_to_snake(cls_name),
            }
            classes.append(class_context)
    context = {"classes": classes}
    return render_template("create_page_views.py.j2", context)
