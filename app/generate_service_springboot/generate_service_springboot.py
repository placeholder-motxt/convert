from app.models.diagram import ClassObject
from app.utils import render_template


def generate_service_java(project_name: str, model: ClassObject) -> str:
    model_name = model.get_name()
    context = {
        "project_name": project_name,
        "class_name_capital": model_name.capitalize(),
        "class_name": model_name[0].lower() + model_name[1:],
    }
    return render_template("springboot/service.java.j2", context)