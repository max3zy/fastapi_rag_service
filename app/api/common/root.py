from fastapi import APIRouter

from app.schemas.root import Root

router = APIRouter()


@router.get("/", response_model=Root)
async def root() -> Root:
    """
    приветственное сообщение - если урл сервиса вставить
    например в браузер - появится приветственное сообщение
    """
    response = Root()
    return response
