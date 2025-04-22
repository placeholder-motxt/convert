import logging
import os
import re
import secrets
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


def render_project_django_template(
    template_path: str, context: dict[str, Any]
) -> dict[str, Any]:
    files = {}
    project_name = context["project_name"]
    if not is_valid_python_identifier(project_name):
        raise ValueError("Project name must not contain whitespace or number!")
    for template_name in os.listdir(template_path):
        template = f"django_project/{template_name}"
        if template_name == "settings.py.j2":
            context = {
                "project_name": project_name,
                "SECRET_KEY": get_random_secret_key(),
            }
        template_name = template_name.replace(".j2", "")
        files[template_name] = (
            # lambda that returns a function that renders the template with the context
            # and returns the rendered template
            lambda t=template, c=context: render_template(t, c) + "\n"
        )
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


def translate_to_cat(msg: str) -> str:
    for category, patterns in ERROR_CATEGORY_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, msg, re.IGNORECASE):
                return category
    return "other"


ERROR_CATEGORY_PATTERNS = [
    (
        "invalid_project",
        [r"Project name must not contain", r"App name must not contain"],
    ),
    ("missing_file", [r"File .+\.zip does not exist"]),
    ("undefined_class", [r"Cannot call class .+ objects not defined"]),
    (
        "invalid_class_file",
        [
            r"Invalid JSON format",
            r"Nodes not found",
            r"Class not found",
            r"ModelsElements does not contain",
            r"Can't create edit views",
        ],
    ),
    ("invalid_sequence_file", [r"The \.sequence\.jet is not valid"]),
    ("invalid_class_name", [r"how to name classes"]),
    (
        "invalid_method_return",
        [r"Method return type not found", r"method name or method return type name"],
    ),
    ("invalid_return_variable", [r"name return variables"]),
    ("too_many_self_call", [r"Too deep self calls"]),
    (
        "invalid_param_name",
        [
            r"Invalid param name",
            r"Parameter name please consult the user",
            r"Parameter name .* name parameters",
            r"please consult the user manual document on how to name parameters",
        ],
    ),
    (
        "invalid_attribute_name",
        [r"attribute name or type is not valid", r"Return edge label must be a valid"],
    ),
    ("invalid_param_type", [r"name parameter types"]),
    ("no_call_edge", [r"Return edge must have a corresponding call edge"]),
    (
        "invalid_relation",
        [r"multiplicity.*relation", r"Invalid use of \*", r"relationship.*wrong"],
    ),
    (
        "invalid_method_name",
        [
            r"name methods",
            r"method cannot be empty",
            r"ClassMethodObject cannot be SET",
        ],
    ),
    ("duplicate_class", [r"Duplicate class name .+ on sequence diagram"]),
    ("invalid_instance_name", [r"instance_name cannot be empty"]),
    ("duplicate_attribute", [r"please remove one of the parameters"]),
]
