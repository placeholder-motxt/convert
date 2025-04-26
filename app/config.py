import os

DEBUG = not os.getenv("PRODUCTION", False)
VERSION = "3.8.8"
APP_CONFIG = {
    "debug": DEBUG,
    "openapi_url": "/openapi.json" if DEBUG else None,
    "version": VERSION,
    "title": "MoTxT Convert",
}
