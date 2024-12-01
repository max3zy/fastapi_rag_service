from fastapi import APIRouter

from app.schemas.root import Root

router = APIRouter()


@router.get("/", response_model=Root)
async def root() -> Root:
    response = Root()
    return response
