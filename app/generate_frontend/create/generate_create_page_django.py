from app.models.elements import ModelsElements
from app.models.diagram import ClassObject, FieldObject
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("app"))

def generate_html_create_pages_django(models_elements: ModelsElements) -> list[str]:
    result = []
    for class_object in models_elements.get_classes():
        result.append(generate_html_create_page_django(class_object))
    return result


def generate_html_create_page_django(class_object: ClassObject) -> str:
    template = env.get_template("create_page_django.html.j2")
    context = {"class_name": class_object.get_name()}
    return template.render(context)


def generate_forms_create_page_django(models_elements: ModelsElements) -> list[str]:
    template = env.get_template('forms.py.j2')
    classes = []
    for class_object in models_elements.get_classes():
        class_context = {"name": class_object.get_name(), "fields": []}
        for field in class_object.get_fields():
            class_context["fields"].append({"name": field.get_name()})
        classes.append(class_context)
    context = {"classes": classes}
    return template.render(context)

if __name__ == "__main__": # pragma: no cover
    class_object = ClassObject()
    class_object.set_name("Person")
    field1 = FieldObject()
    field1.set_name("name")
    field2 = FieldObject()
    field2.set_name("age")
    field3 = FieldObject()
    field3.set_name("is_alive")
    class_object.add_field(field1)
    class_object.add_field(field2)
    class_object.add_field(field3)
    models_element = ModelsElements("Person")
    models_element.add_class(class_object)
    models_element.add_class(class_object)
    print(generate_forms_create_page_django(models_element))
