from app.api.v1.endpoints import classify
from fastapi import APIRouter


def config_routers_v1() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(classify.router)
    return api_router
