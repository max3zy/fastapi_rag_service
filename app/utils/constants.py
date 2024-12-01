from enum import Enum

class TargetLabels(int, Enum):
    TARGET_1 = 1
    TARGET_0 = 0


class DebugLevel(int, Enum):
    LVL_0 = 0
    LVL_1 = 1

    def is_high_level(self) -> bool:
        return self != self.LVL_0


class PromptType(str, Enum):
    DEFAULT = "default_llama"


class SearchStrategy(str, Enum):
    OPEN_SEARCH = "open_search_vector"

    def is_use_embedding(self) -> bool:
        return "vector" in self


class CacheStrategy(str, Enum):
    REDIS = "redis"
    NO_CACHE = "no_cache"



