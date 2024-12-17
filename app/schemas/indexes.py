from dataclasses import dataclass


@dataclass
class OpenSearchIndexes:
    VECTOR_INDEX: str
    FULL_TEXT_INDEX: str
    PREFIX_INDEX: str
