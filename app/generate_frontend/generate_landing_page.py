from app.models.diagram import ClassObject
from app.utils import render_template


def generate_landing_page_html() -> str:
    return render_template("landing_page.html.j2", {})


def generate_landing_page_views(classes: list[ClassObject]) -> str:
    return render_template("landing_page_views.py.j2", {"classes": classes})
