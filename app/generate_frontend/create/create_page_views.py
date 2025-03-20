from jinja2 import Environment, PackageLoader

from app.models.elements import ModelsElements
from app.utils import camel_to_snake

env = Environment(loader=PackageLoader("app"))


def generate_create_page_views(models_elements: ModelsElements) -> str:
    template = env.get_template("create_page_views.py.j2")
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
    return template.render(context)
