import os
import secrets
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
        os.makedirs(folder_path)
    except OSError:
        raise FileExistsError(f"Folder {folder_path} already exists")
    for template_name in os.listdir(template_path):
        file_path = os.path.join(template_path, template_name)
        file_path = file_path.replace("\\", "/")
        if os.path.isfile(file_path):
            template = env.get_template(f"django_project/{template_name}")
            if template_name == "settings.py.j2":
                context = {
                    "project_name": context["project_name"],
                    "SECRET_KEY": get_random_secret_key(),
                }
            template_name = template_name.replace(".j2", "")
            with open(os.path.join(folder_path, template_name), "w") as file:
                file.write(template.render(context))
                file.write("\n")  # add newline at the end of file for linter
            files.append(template_name)
        else:
            raise ValueError(f"Template {template_name} is not a file")
    return files


# method to generate random secret key taken from Django
RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_secret_key() -> str:  # pragma: no cover
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return get_random_string(50, chars)


def get_random_string(
    length: int, allowed_chars: str = RANDOM_STRING_CHARS
) -> str:  # pragma: no cover
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))
