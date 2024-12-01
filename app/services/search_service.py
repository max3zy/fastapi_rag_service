from typing import Any, List, Optional

from opensearchpy import AsyncOpenSearch, OpenSearch


class OpenSearchApiClient:
    INDEX_NAME = "test_faqs_v1"
    HOST = "localhost"
    TIMEOUT = 1000
    MAX_RETRIES = 2
    SIZE = 1

    def __init__(self):
        self.client = AsyncOpenSearch(
            self.HOST,
            max_retries=self.MAX_RETRIES,
            retry_on_timeout=True,
            timeout=self.TIMEOUT,
            read_timeout=self.TIMEOUT,
        )

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

        response = await self.client.search(index=self.INDEX_NAME, body=body)
        # print(response)
        return response["hits"]["hits"]