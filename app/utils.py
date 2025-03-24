import os
import re
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


def camel_to_snake(camel_case_str: str) -> str:
    # Adjust regex to handle acronyms properly (uppercase letters in the middle of the string)
    snake_case_str = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", camel_case_str)
    # Special handling for acronyms: Make sure that sequences of uppercase letters are also split
    # correctly.
    snake_case_str = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", snake_case_str)
    return snake_case_str.lower()
