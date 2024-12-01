from app.config import settings
from pydantic import BaseModel, Field


class Root(BaseModel):
    message: str = Field(
        f"rag-service v {settings.SERVICE_VERSION} Команды навыков",
        description="Приветственное сообщение от сервера",
        example=f" v {settings.SERVICE_VERSION}",
    )
