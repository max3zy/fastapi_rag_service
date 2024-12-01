from fastapi import APIRouter

from app.api.common import health, root
from app.api.v1.api import config_routers_v1


def add_common_services(api_router: APIRouter):
    api_router.include_router(root.router)
    api_router.include_router(health.router)


def add_endpoints_v1(api_router: APIRouter):
    api_router.include_router(config_routers_v1(), prefix="/v1")


def config_routers() -> APIRouter:
    api_router = APIRouter()
    add_common_services(api_router)
    add_endpoints_v1(api_router)
    return api_router
