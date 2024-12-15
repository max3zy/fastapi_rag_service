from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from opensearchpy import AsyncOpenSearch

from app.config import settings
from app.schemas.common.documents import Document


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

    @abstractmethod
    def build_filters(self, category: str) -> Dict[str, Any]:
        pass

    async def get_response_hits(self, body) -> List[Dict[str, Any]]:
        response = await self.client.search(index=self.index, body=body)
        return response["hits"]["hits"]


class OpenSearchVectorApiClient(OpenSearchApiClient):
    NO_FILTER = {"match_all": {}}

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
            "size": num_docs,
            # "_source": ["title", "text", "type"],
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

        response = await self.client.search(index=self.index, body=body)
        documents = response["hits"]["hits"]
        return [
            Document(
                text=item["_source"]["text_filtered"],
                title=item["_source"]["title3_zagolovok"],
                category=item["_source"]["title1"],
                similarity=item["_score"],
            )
            for item in documents
        ]

    def build_filters(self, category: str) -> Dict[str, Any]:
        return {"bool": {"filter": {"term": {"title1": category}}}}


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
        body = {
            "size": num_docs * 2,
            "query": {
                "knn": {
                    "distiluse_embs_v1": {"vector": embedding, "k": num_docs}
                }
            },
        }

        response = await self.client.search(index=self.index, body=body)
        # print(response)
        return response["hits"]["hits"]

    def build_filters(self, category: str) -> Dict[str, str]:
        pass


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
        body = {"query": {"prefix": {"title3_zagolovok": query}}}

        response = await self.client.search(index=self.index, body=body)
        # print(response)
        documents = response["hits"]["hits"]
        return [
            Document(
                text=item["_source"]["text_filtered"],
                title=item["_source"]["title3_zagolovok"],
                category=item["_source"]["title1"],
                similarity=item["_score"],
            )
            for item in documents
        ]

    def build_filters(self, category: str) -> Dict[str, str]:
        pass


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
                    ]
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
        response = await self.client.search(
            index=self.index, body=body, size=num_docs
        )

        documents = response["hits"]["hits"]
        return [
            Document(
                text=item["_source"]["text_filtered"],
                title=item["_source"]["title3_main"],
                category=item["_source"]["title1"],
                similarity=item["_score"],
            )
            for item in documents
        ]

    def build_filters(self, category: str) -> Dict[str, str]:
        pass
