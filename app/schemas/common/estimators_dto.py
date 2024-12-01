from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from app.schemas.categories import Category
from app.schemas.common.documents import Document
from app.schemas.intent_classifier import IntentClf
from app.utils.constants import CacheStrategy, DebugLevel, SearchStrategy


class EstimatorIn(BaseModel):
    query: str
    num_docs: int
    search_strategy: SearchStrategy
    cache_strategy: CacheStrategy
    category: Category
    intent_classifier: IntentClf
    session_id: str
    system_prompt: str
    debug_level: DebugLevel
    debug_info: Optional[Dict[str, Any]]


class StrategyIn(BaseModel):
    query: str
    answer: str
    documents: List[Document]
    session_id: str
    debug_level: DebugLevel
    debug_info: Optional[Dict[str, Any]]


class StrategyOut(BaseModel):
    answer: str
    documents: List[Document]
    session_id: str
    debug_level: DebugLevel
    debug_info: Optional[Dict[str, Any]]
