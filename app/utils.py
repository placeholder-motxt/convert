import os

def remove_file(path: str) -> None:
    os.unlink(path)