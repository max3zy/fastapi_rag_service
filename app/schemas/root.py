from pydantic import BaseModel, Field

from app.config import settings


class Root(BaseModel):
    message: str = Field(
        f"rag-service v {settings.SERVICE_VERSION}",
        description="Приветственное сообщение от сервера",
        example=f" v {settings.SERVICE_VERSION}",
    )
