from pydantic import BaseModel, Field

from app.config import settings


class HelloWorld(BaseModel):
    message: str = Field(
        "Hello world!",
        description="Приветственное сообщение от сервера",
        example=f" v {settings.SERVICE_VERSION}",
    )
