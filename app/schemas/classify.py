from typing import Union

from pydantic import BaseModel, Field


class ClassifyResponse(BaseModel):
    classify_score: Union[int, float] = Field(
        ...,
        description="Все варианты для дополнения текста пользователя",
    )
