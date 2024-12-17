from enum import Enum


class StatusCode(str, Enum):
    CENSORED = "CENSORED"
    PASSED = "PASSED"
    NO_INFO = "NO_INFO"
    NO_ANSWER = "NO_ANSWER"


class DebugLevel(int, Enum):
    LVL_0 = 0
    LVL_1 = 1

    def is_high_level(self) -> bool:
        return self != self.LVL_0


class PromptType(str, Enum):
    DEFAULT = "default_llama"


class SearchStrategy(str, Enum):
    OPEN_SEARCH_VECTOR = "vector"
    OPEN_SEARCH_HYBRID = "hybrid"
    OPEN_SEARCH_FULL_TEXT = "full_text"
    OPEN_SEARCH_PREFIX = "prefix"

    def is_use_embedding(self) -> bool:
        return "vector" in self


class CacheStrategy(str, Enum):
    REDIS = "redis"
    NO_CACHE = "no_cache"


class Vectorizer(str, Enum):
    DISTILUSE_BASE = "distiluse_base"
    DISTILUSE_FINETUNED = "distiluse_tuned"


DOCUMENT_SEPARATOR = "\n\n"
EMPTY_STRING = ""
SPACE = " "
STRING_SEPARATOR = "\n"