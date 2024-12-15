import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.categories import Category
from app.schemas.censor import Censor
from app.schemas.common.documents import Document
from app.schemas.intent_classifier import IntentClf
from app.utils.constants import (
    CacheStrategy,
    DebugLevel,
    PromptType,
    SearchStrategy,
    StatusCode,
    Vectorizer,
)


class RagRequest(BaseModel):
    query: str = Field(None, description="запрос пользователя")
    use_llm: bool = True
    sim_threshold: float = 0
    num_docs: Optional[int] = Field(
        5, description="кол-во документов поисковой выдачи"
    )
    search_strategy: Optional[SearchStrategy] = Field(
        SearchStrategy.OPEN_SEARCH_VECTOR,
        description="стратегия поиска документов",
    )
    # llm_providedr: Optional[LlmProvider] = Field(
    #     LlmProvider.LLAMA_2, description=""
    # )
    vectorize_strategy: Optional[Vectorizer] = Field(
        Vectorizer.DISTILUSE_FINETUNED,
        description="выбор модельки векторизации",
    )
    censor: Optional[Censor] = Field(
        Censor(),
        description=(
            "использование и параметры классификатора вредоносных запросов"
        ),
    )
    cache_strategy: Optional[CacheStrategy] = Field(
        CacheStrategy.NO_CACHE, description="стратегия кэширования ответов ЛЛМ"
    )
    category: Optional[Category] = Field(
        Category(), description="категория запроса пользователя"
    )
    intent_classifier: Optional[IntentClf] = Field(
        IntentClf(),
        description=(
            "использование и параметры классификатора категории запроса"
        ),
    )
    session_id: Optional[str] = Field(
        str(uuid.uuid4()),
        description="Сессия пользователя",
    )
    prompt_type: PromptType = Field(
        PromptType.DEFAULT,
        description="промпт, передающийся в ЛЛМ",
    )
    debug_level: DebugLevel = Field(
        DebugLevel.LVL_0, description="использование отладочной информации"
    )


class RagResponse(BaseModel):
    answer: str
    item_list: List[Document]
    status_code: StatusCode
    debug_info: Optional[Dict[str, Any]] = None
