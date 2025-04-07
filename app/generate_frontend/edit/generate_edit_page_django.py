from app.models.diagram import ClassObject
from app.models.elements import ModelsElements
from app.utils import render_template


def generate_html_edit_pages_django(models_elements: ModelsElements) -> list[str]:
    """
    Generates edit page HTML of all ClassObject inside of ModelsElement
    If a ClassObject somehow doesn't have a name nor fields, the edit
    page will not be generated.

    Returns a list of string where each string is HTML that corresponds
    to each non empty ClassObject in ModelsElement.
    """

    result = []
    for class_object in models_elements.get_classes():
        if class_object.get_is_public():
            html = generate_html_edit_page_django(class_object)
            if html != "":
                result.append(html)

    return result


def generate_html_edit_page_django(class_object: ClassObject) -> str:
    """
    Generates edit page HTML of a ClassObject if it has a name and fields.

    Returns a string representation of the HTML page or an empty string
    if the ClassObject doesn't have a name nor fields.
    """

    if class_object.get_name() == "" or len(class_object.get_fields()) == 0:
        return ""

    context = {"class_name": class_object.get_name()}
    return render_template("edit_page_django.html.j2", context)
