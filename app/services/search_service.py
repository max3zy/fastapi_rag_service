from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from opensearchpy import AsyncOpenSearch

from app.config import settings
from app.schemas.common.documents import Document
from app.schemas.search import OpenSearchResponse
from app.utils.base_model import singleton


class OpenSearchApiClient(ABC):
    def __init__(self, index):
        self.index = index
        self.client = AsyncOpenSearch(
            settings.OPEN_SEARCH_HOST,
            max_retries=settings.OPEN_SEARCH_RETRIES,
            retry_on_timeout=True,
            timeout=settings.OPEN_SEARCH_TIMEOUT,
            read_timeout=settings.OPEN_SEARCH_TIMEOUT,
        )

    @abstractmethod
    async def request(
        self,
        query: str,
        num_docs: int,
        embedding: Optional[List[float]],
        category: str,
    ) -> List[Document]:
        pass

    async def get_response_docs(
        self, body: Dict[str, Any], size: int = None
    ) -> List[Dict[str, Any]]:
        res = await self.client.search(index=self.index, body=body, size=size)
        response = OpenSearchResponse(**res)
        return [
            Document(
                text=item.source.text_filtered,
                title=item.source.title3_zagolovok,
                category=item.source.title1,
                similarity=item.score,
            )
            for item in response.hits.hits
        ]


@singleton
class OpenSearchVectorApiClient(OpenSearchApiClient):
    NO_FILTER = {"match_all": {}}

    def __init__(self, index):
        super().__init__(index)

    async def request(
        self,
        query: str,
        num_docs: int,
        embedding: Optional[List[float]],
        category: Optional[str],
    ) -> List[Any]:
        body = {
            "size": num_docs,
            "query": {
                "script_score": {
                    "query": (
                        self.NO_FILTER
                        if category is None
                        else self.build_filters(category)
                    ),
                    "script": {
                        "lang": "knn",
                        "source": "knn_score",
                        "params": {
                            "field": "embeddings",
                            "query_value": embedding,
                            "space_type": "l2",
                        },
                    },
                }
            },
        }
        return await self.get_response_docs(body)

    @staticmethod
    def build_filters(category: str) -> Dict[str, Any]:
        return {"bool": {"filter": {"term": {"title1": category}}}}


@singleton
class OpenSearchHybridApiClient(OpenSearchApiClient):
    def __init__(self, index):
        super().__init__(index)

    async def request(
        self,
        query: str,
        num_docs: int,
        embedding: Optional[List[float]],
        category: str,
    ) -> List[Any]:
        pass

    @staticmethod
    def build_filters(category: str) -> Dict[str, str]:
        pass


@singleton
class OpenSearchPrefixApiClient(OpenSearchApiClient):
    def __init__(self, index):
        super().__init__(index)

    async def request(
        self,
        query: str,
        num_docs: int,
        embedding: Optional[List[float]],
        category: str,
    ) -> List[Any]:
        body = {
            "query": {"bool": {"must": self.build_filters(query, category)}}
        }

        return await self.get_response_docs(body, size=num_docs)

    @staticmethod
    def build_filters(query: str, category: str) -> List[Any]:
        filters = [
            {"prefix": {"title3_zagolovok": query}},
            {"match": {"title1": category}} if category else None,
        ]
        return [el for el in filters if el is not None]


@singleton
class OpenSearchFullTextApiClient(OpenSearchApiClient):
    def __init__(self, index):
        super().__init__(index)

    async def request(
        self,
        query: str,
        num_docs: int,
        embedding: Optional[List[float]],
        category: str,
    ) -> List[Any]:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "analyzer": "ru_analyzer_stem",
                                "fields": [
                                    "title3_zagolovok^2",
                                    "text_filtered",
                                ],
                                "query": query,
                                "fuzziness": "AUTO",
                            }
                        }
                    ],
                    "filter": [self.build_filters(category)],
                }
            },
            "highlight": {
                "order": "score",
                "fields": {
                    "text": {
                        "type": "plain",
                        "fragment_size": 150,
                        "number_of_fragments": 1,
                    }
                },
            },
        }
        return await self.get_response_docs(body, size=num_docs)

    @staticmethod
    def build_filters(category: str) -> Optional[Dict[str, Any]]:
        return (
            {"term": {"title1": category}} if category else {"match_all": {}}
        )
