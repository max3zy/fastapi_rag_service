from typing import List

from sentence_transformers import SentenceTransformer

from app.config import settings
from app.utils.constants import Vectorizer


class TransformersVectorization:
    def __init__(self):
        self.model = {
            Vectorizer.DISTILUSE_BASE: SentenceTransformer(
                "sentence-transformers/distiluse-base-multilingual-cased-v1"
            ),
            Vectorizer.DISTILUSE_FINETUNED: SentenceTransformer(
                settings.DISTILUSE_FINETUNED_740, local_files_only=True
            ),
        }

    def emb(self, query: str, vectorize_strategy: Vectorizer) -> List[float]:
        return self.model[vectorize_strategy].encode(query).tolist()
