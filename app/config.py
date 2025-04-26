import os

DEBUG = not os.getenv("PRODUCTION", False)
VERSION = "3.8.8"
APP_CONFIG = {
    "debug": DEBUG,
    "openapi_url": "/openapi.json" if DEBUG else None,
    "version": VERSION,
    "title": "MoTxT Convert",
}
SPRING_SERVICE_URL = os.getenv("SPRING_SERVICE_URL", "http://localhost:8080")
SPRING_DEPENDENCIES = (
    "lombok,devtools,configuration-processor,web,data-jpa,validation,"
    "springdoc-starter-webmvc-ui,hibernate-core,hibernate-community-dialects,"
    "hikaricp,sqlite,jakarta-persistence-api"
)
