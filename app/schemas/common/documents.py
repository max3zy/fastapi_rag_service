from pydantic import BaseModel


class Document(BaseModel):
    text: str
    title: str
    category: str
    similarity: float

    def __lt__(self, other) -> bool:
        return self.similarity > other.similarity
