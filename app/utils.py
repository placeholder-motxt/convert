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
