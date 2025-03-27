import logging
import os
import re
from keyword import iskeyword
from typing import Any

from jinja2 import Environment, PackageLoader, TemplateNotFound

env = Environment(loader=PackageLoader("app"))  # nosec B701 - not used for rendering HTML to the user
logger = logging.getLogger("uvicorn.error")


def remove_file(path: str) -> None:
    os.unlink(path)


def is_valid_python_identifier(identifier: str) -> bool:
    return identifier.isidentifier() and not iskeyword(identifier)


def render_template(
    template_name: str, context: dict[str, Any] = {}, **kwargs: dict[str, Any]
) -> str:
    context |= kwargs
    try:
        template = env.get_template(template_name)
        return template.render(context)
    except TemplateNotFound as e:  # Somehow the template can't be found
        logger.error(f"Template not found: {e}")
        # TODO: Maybe send alert to us
        return ""
    except Exception as e:  # All other cases
        logger.warning(f"An error occured: {e}")
        return ""


def camel_to_snake(camel_case_str: str) -> str:
    if not isinstance(camel_case_str, str):
        raise TypeError("Input must be a string")
    # Adjust regex to handle acronyms properly (uppercase letters in the middle of the string)
    snake_case_str = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", camel_case_str)

    # Special handling for acronyms: Make sure that sequences of uppercase letters are also split
    # correctly.
    snake_case_str = re.sub(r"([A-Z]+)(?=[A-Z])", r"\1_", snake_case_str)
    return snake_case_str.lower()
