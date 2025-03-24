from app.models.diagram import ClassObject, FieldObject
from app.models.elements import ModelsElements
from app.utils import camel_to_snake, render_template


def generate_html_read_pages_django(models_elements: ModelsElements) -> list[str]:
    result = []
    for class_object in models_elements.get_classes():
        result.append(generate_html_read_page_django(class_object))
    return result


def generate_html_read_page_django(class_object: ClassObject) -> str:
    context = {
        "class_name": class_object.get_name(),
        "class_snake": camel_to_snake(class_object.get_name()),
    }
    fields = []
    for field in class_object.get_fields():
        fields.append({"name": field.get_name()})
    context["fields"] = fields
    return render_template("read_page_django.html.j2", context)


if __name__ == "__main__":
    model = ClassObject()
    model.set_name("Person")
    field1 = FieldObject()
    field1.set_name("name")
    field2 = FieldObject()
    field2.set_name("age")
    field3 = FieldObject()
    field3.set_name("is_alive")

    model.add_field(field1)
    model.add_field(field2)
    model.add_field(field3)

    print(generate_html_read_page_django(model))
