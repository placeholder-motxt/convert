from app.models.diagram import ClassObject
from app.utils import render_template


# Call this to generate SwaggerConfig.java
def generate_swagger_config(project_name: str) -> str:
    context = {"project_name": project_name}
    return render_template("SwaggerConfig.java.j2", context)


# I made this function just in case when integration we forgot to
# add the swagger import to controller, I hope be this function will remind us of it
def get_swagger_controller_import() -> str:
    return "import io.swagger.v3.oas.annotations.Operation;\n"


# Call this in the iteration when creating each class's controller
def get_swagger_decorators(model: ClassObject) -> dict:
    return {
        "create_swagger": f'@Operation(summary = "Create a new {model.get_name()}")',
        "read_swagger": f'@Operation(summary = "Get a {model.get_name()} by ID")',
        "update_swagger": f'@Operation(summary = "Update an existing {model.get_name()}")',
        "delete_swagger": f'@Operation(summary = "Delete a {model.get_name()} by ID")',
    }
