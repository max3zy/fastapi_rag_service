from fastapi import APIRouter

router = APIRouter()


# Add Health Check
# TODO fastapi-async-healthcheck
@router.get("/health")
async def health():
    return "OK"
