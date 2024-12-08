from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, List, Optional

import ahocorasick
import pandas as pd
from mypy.errorcodes import ABSTRACT
from opensearchpy import AsyncOpenSearch, OpenSearch
from thefuzz import fuzz

from app.config import settings
from app.schemas.common.documents import Document
from app.utils.preprocess.preprocessing import text_cleanup_preprocessor


class OpenSearchApiClient(ABC):
    def __init__(self, host, max_retries, timeout, index):
        self.index = index
        self.client = AsyncOpenSearch(
            host,
            max_retries=max_retries,
            retry_on_timeout=True,
            timeout=timeout,
            read_timeout=timeout,
        )

    @abstractmethod
    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
    ):
        pass

    async def get_response_hits(self, body) -> List[Dict[str, Any]]:
        response = await self.client.search(index=self.index, body=body)
        return response["hits"]["hits"]


class TableSearchClient(ABC):
    def __init__(self, table_path, keys_for_filter):
        self.table = pd.read_parquet(table_path)
        self.table_columns = self.table.columns.tolist()
        self.keys_for_filter = keys_for_filter

    @abstractmethod
    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
    ):
        pass

    @abstractmethod
    def make_indexes(self):
        pass

    def make_keys_to_indexes(self):
        keys_to_indexes = {}
        for key in self.keys_for_filter:
            keys_to_indexes[key] = defaultdict(list)
            for ndx, val in self.table[key].items():
                keys_to_indexes[key][val].append(ndx)
        self.keys_to_indexes = {
            key: {k: v for k, v in val.items()}
            for key, val in keys_to_indexes.items()
        }


class FaissVectorClient(TableSearchClient):
    def __init__(self, table_path, keys_for_filter):
        super().__init__(table_path, keys_for_filter)

    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
    ):
        pass

    def make_indexes(self):
        pass


class PrefixClient(TableSearchClient):
    def __init__(self, table_path, keys_for_filter):
        super().__init__(table_path, keys_for_filter)
        self.automaton = ahocorasick.Automaton()
        self.make_indexes()

    def make_indexes(self):
        for key in self.keys_for_filter:
            for index, row in self.table.iterrows():
                val = text_cleanup_preprocessor(row[key])
                self.automaton.add_word(
                    val,
                    (
                        row["text_filtered"],
                        row["title3_main"],
                        row["title1"],
                    ),
                )
        self.automaton.make_automaton()

    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
    ):
        documents = list(self.automaton.items(query))
        return [
            Document(
                text=text,
                title=title3,
                category=title1,
                similarity=fuzz.ratio(query, _) / 100,
            )
            for _, (text, title3, title1) in documents
        ]


class OpenSearchVectorApiClient(OpenSearchApiClient):
    # INDEX_NAME = "test_faqs_v1"
    # HOST = "localhost"
    # TIMEOUT = 1000
    # MAX_RETRIES = 2
    # SIZE = 1

    def __init__(self, host, max_retries, timeout, index):
        # self.client = AsyncOpenSearch(
        #     self.HOST,
        #     max_retries=self.MAX_RETRIES,
        #     retry_on_timeout=True,
        #     timeout=self.TIMEOUT,
        #     read_timeout=self.TIMEOUT,
        # )
        super().__init__(host, max_retries, timeout, index)

    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
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


class OpenSearchHybridApiClient(OpenSearchApiClient):
    # INDEX_NAME = "test_faqs_v1"
    # HOST = "localhost"
    # TIMEOUT = 1000
    # MAX_RETRIES = 2
    # SIZE = 1

    def __init__(self, host, max_retries, timeout, index):
        # self.client = AsyncOpenSearch(
        #     self.HOST,
        #     max_retries=self.MAX_RETRIES,
        #     retry_on_timeout=True,
        #     timeout=self.TIMEOUT,
        #     read_timeout=self.TIMEOUT,
        # )
        super().__init__(host, max_retries, timeout, index)

    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
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


class OpenSearchFullTextApiClient(OpenSearchApiClient):
    def __init__(self, host, max_retries, timeout, index):
        super().__init__(host, max_retries, timeout, index)

    async def request(
        self, query: str, num_docs: int, embedding: Optional[List[float]]
    ) -> List[Any]:
        body = {
            "size": num_docs * 2,
            "query": {
                "knn": {
                    "distiluse_embs_v1": {"vector": embedding, "k": num_docs}
                }
            },
        }
        return await self.get_response_hits(body)

        # response = await self.client.search(index=self.index, body=body)
        # return response["hits"]["hits"]
