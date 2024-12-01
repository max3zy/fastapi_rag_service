from typing import List

from sentence_transformers import SentenceTransformer

class TransformersVectorization:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased-v1")

    def emb(self, query: str) -> List[float]:
        return self.model.encode(query).tolist()