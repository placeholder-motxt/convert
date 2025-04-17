from app.utils import render_template


# Call this to generate SwaggerConfig.java
def generate_swagger_config(project_name: str) -> str:
    context = {"project_name": project_name}
    return render_template("SwaggerConfig.java.j2", context)
