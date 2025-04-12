from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_read_page_views(models_elements: ModelsElements) -> str:
    if not isinstance(models_elements, ModelsElements):
        raise TypeError(
            f"Expected type ModelsElements, got {type(models_elements)} instead"
        )

    class_list = []
    for class_object in models_elements.get_classes():
        if class_object.get_is_public():
            cls_name = class_object.get_name()
            class_list.append(
                {
                    "class_name": cls_name,
                    "class_snake": camel_to_snake(cls_name),
                }
            )
    context = {"classes": class_list}
    return render_template("read_page_views.py.j2", context)
