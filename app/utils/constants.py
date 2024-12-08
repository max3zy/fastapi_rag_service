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
    OPEN_SEARCH_VECTOR = "open_search_vector"
    OPEN_SEARCH_HYBRID = "open_search_hybrid"
    OPEN_SEARCH_FULL_TEXT = "open_search_full_text"
    FAISS_TABLE_VECTOR = "faiss_table_vector"
    TABLE_PREFIX = "table_prefix"

    def is_use_embedding(self) -> bool:
        return "vector" in self


class CacheStrategy(str, Enum):
    REDIS = "redis"
    NO_CACHE = "no_cache"
