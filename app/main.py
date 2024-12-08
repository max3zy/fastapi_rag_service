import uvicorn

# from da_robot_max_chain.da_log.logger import logger_factory
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.application_api import config_routers
from app.api.containers import AppContainer
from app.api.v1.endpoints import classify
from app.config import settings

# logger = logger_factory(__name__)


def add_all_routers(app: FastAPI) -> None:
    app.include_router(
        config_routers(),
    )


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def app_factory() -> FastAPI:
    container = AppContainer()
    container.wire([classify])
    container.rag()

    app = FastAPI(
        title=settings.SERVICE_TITLE,
        description=settings.SERVICE_DESCRIPTION,
        version=settings.SERVICE_VERSION,
    )
    add_all_routers(app)
    add_middleware(app)
    return app


def run_server() -> None:
    uvicorn.run(
        settings.RUN_SERVER_COMMAND,
        host=settings.RUN_SERVER_HOST,
        port=settings.RUN_SERVER_PORT,
        access_log=settings.RUN_SERVER_ACCESS_LOG,
        log_level=settings.RUN_SERVER_LOG_LEVEL,
        factory=settings.RUN_SERVER_FACTORY,
        reload=settings.RUN_SERVER_DEBUG_RELOAD,
    )


if __name__ == "__main__":
    run_server()
