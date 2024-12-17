from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


class FaqDocumentSource(BaseModel):
    text_filtered: str
    title1: str
    title3_zagolovok: Optional[str] = None
    title3_main: Optional[str] = None


class HitTotal(BaseModel):
    value: int
    relation: str


class Hit(BaseModel):
    index: str = Field(..., alias="_index")
    id: str = Field(..., alias="_id")
    score: float = Field(..., alias="_score")
    source: FaqDocumentSource = Field(..., alias="_source")


class Hits(BaseModel):
    total: HitTotal
    max_score: Union[float, None]
    hits: Union[List[Hit], None]


class OpenSearchResponse(BaseModel):
    took: int
    timed_out: bool
    _shards: Any
    hits: Hits
