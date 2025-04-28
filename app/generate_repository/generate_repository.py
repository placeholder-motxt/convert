from app.models.diagram import ClassObject
from app.utils import (
    render_template,
    to_pascal_case,
)


def generate_repository_java(
    project_name: str, model: ClassObject, group_id: str
) -> str:
    context = {
        "project_name": project_name,
        "class_name": to_pascal_case(model.get_name()),
        "group_id": group_id,
    }
    return render_template("repository.java.j2", context)
