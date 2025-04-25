from app.utils import (
    render_template,
)


def generate_sqlitedialect(project_name: str, trailing_project_name: str) -> str:
    context = {
        "project_name": project_name,
        "trailing_project_name": trailing_project_name,
    }
    return render_template("SQLiteDialect.java.j2", context)
