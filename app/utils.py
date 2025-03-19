import os
from keyword import iskeyword
from typing import Any

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("app"))


def remove_file(path: str) -> None:
    os.unlink(path)


def is_valid_python_identifier(identifier: str) -> bool:
    return identifier.isidentifier() and not iskeyword(identifier)


def render_template(template_name: str, context: dict[str, Any]) -> str:
    template = env.get_template(template_name)
    return template.render(context)


def render_project_django_template(
    template_path: str, context: dict[str, Any]
) -> list[str]:
    files = []
    if not is_valid_python_identifier(context["project_name"]):
        raise ValueError("Project name must not contain whitespace or number!")
    folder_path = f"project_{context['project_name']}"
    try:
        print(os.path.exists(folder_path))
        # os.startfile(folder_path)
        os.makedirs(folder_path)
    except OSError as e:
        raise FileExistsError(e.strerror)
    for template_name in os.listdir(template_path):
        file_path = os.path.join(template_path, template_name)
        file_path = file_path.replace("\\", "/")
        if os.path.isfile(file_path):
            template = env.get_template(f"django_project/{template_name}")
            if template_name == "settings.py.j2":
                context = {
                    "project_name": context["project_name"],
                    "SECRET_KEY": "",
                }
            template_name = template_name.replace(".j2", "")
            with open(os.path.join(folder_path, template_name), "w") as file:
                file.write(template.render(context))
            files.append(template_name)
        else:
            raise ValueError(f"Template {template_name} is not a file")
    return files
