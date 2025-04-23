# put this inside file run.bat
from app.utils import render_template


def generate_springboot_window_runner() -> str:
    return render_template("springboot_scripts/run.bat.txt")


# put this inside file run.sh
def generate_springboot_linux_runner() -> str:
    return render_template("springboot_scripts/run.sh.txt")
