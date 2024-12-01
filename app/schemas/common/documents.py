from pydantic import BaseModel


class Document(BaseModel):
    text: str
    title: str
    category: str
    similarity: float
