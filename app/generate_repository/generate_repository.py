from app.models.diagram import ClassObject
from app.utils import (
    render_template,
    to_pascal_case,
)


def generate_repository_java(project_name: str, model: ClassObject) -> str:
    context = {
        "project_name": project_name,
        "class_name": to_pascal_case(model.get_name()),
    }
    return render_template("repository.java.j2", context)
