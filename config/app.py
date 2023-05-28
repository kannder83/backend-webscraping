# Logs
import logging

# Libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.conf import settings


# Routes
from app.web_scraping.routes import router as hello_router
# from app.security.routes import router as security_router
# from app.user.routes import router as user_router
# from app.classroom.routes import router as classroom_router
# from app.subject.routes import router as subject_router


def get_application():

    api_conf: dict = {
        "title": "DEV: WebScraping",
        "description": "DEV: WebScraping",
        "root_path": settings.dev_url,
        "docs_url": settings.dev_url
    }

    origins: list = ["*"]

    if not settings.debug:
        api_conf: dict = {
            "title": "WebScraping",
            "description": "WebScraping",
            "root_path": settings.prod_url,
            "docs_url": settings.prod_url
        }

        origins: list = settings.allowed_hosts

    app: FastAPI = FastAPI(
        title=api_conf["title"],
        description=api_conf["description"],
        docs_url=api_conf["docs_url"],
        root_path=api_conf["root_path"]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    def startup_event():

        if settings.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(message)s"
            )
        else:
            logging.basicConfig(
                level=logging.WARNING,
                format="%(asctime)s %(levelname)s %(message)s"
            )

    # Routes to publish
    app.include_router(hello_router)
    # app.include_router(security_router)
    # app.include_router(user_router)
    # app.include_router(classroom_router)
    # app.include_router(subject_router)

    return app


application = get_application()
