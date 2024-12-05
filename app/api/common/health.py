from fastapi import APIRouter

router = APIRouter()


# Add Health Check
# TODO fastapi-async-healthcheck
@router.get("/health")
async def health():
    """ обычный хэлс чек - если этот эндпоинт не отвечает, значит сервису херовенько"""
    return "OK"
