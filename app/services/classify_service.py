from abc import ABC
from typing import Dict, List, Union

from app.config import settings
from app.schemas.common.documents import Document
from app.schemas.common.estimators_dto import EstimatorIn, StrategyIn
from app.services.llm_providers import LlamaProvider
from app.services.redis.redis_service import CacheRedis, NoCache
from app.services.search_service import (
    FaissVectorClient,
    OpenSearchApiClient,
    OpenSearchFullTextApiClient,
    OpenSearchHybridApiClient,
    OpenSearchVectorApiClient,
    PrefixClient,
    TableSearchClient,
)
from app.services.vectorization_service import TransformersVectorization
from app.utils.constants import CacheStrategy, SearchStrategy


class Rag(ABC):
    def __init__(self, redis_service):
        self.search_service: Dict[
            SearchStrategy, Union[TableSearchClient, OpenSearchApiClient]
        ] = {
            SearchStrategy.OPEN_SEARCH_VECTOR: OpenSearchVectorApiClient(
                index="test_faqs_v1",
                host="localhost",
                timeout=1000,
                max_retries=2,
            ),
            SearchStrategy.OPEN_SEARCH_HYBRID: OpenSearchHybridApiClient(
                index="test_faqs_v1",
                host="localhost",
                timeout=1000,
                max_retries=2,
            ),
            SearchStrategy.OPEN_SEARCH_FULL_TEXT: OpenSearchFullTextApiClient(
                index="test_faqs_v1",
                host="localhost",
                timeout=1000,
                max_retries=2,
            ),
            SearchStrategy.FAISS_TABLE_VECTOR: FaissVectorClient(
                table_path=settings.PATH_TO_INDEX,
                keys_for_filter=("title3_zagolovok",),
            ),
            SearchStrategy.TABLE_PREFIX: PrefixClient(
                table_path=settings.PATH_TO_INDEX,
                keys_for_filter=("title3_zagolovok",),
            ),
        }
        self.vectorize_service = TransformersVectorization()
        self.llm_model = LlamaProvider()
        self.cache_system = {
            CacheStrategy.REDIS: CacheRedis(redis=redis_service),
            CacheStrategy.NO_CACHE: NoCache(),
        }

    async def get_answer(self, rag_input: EstimatorIn) -> StrategyIn:
        if not rag_input.category.category and rag_input.intent_classifier.use:
            pass  # todo intent classifiactor returns user category: ex - rag_input.category.category = clf.returned_score

        similar_documents = await self.found_similar_docs(rag_input)

        system_cache = self.cache_system.get(
            rag_input.cache_strategy, CacheStrategy.NO_CACHE
        )
        llm_answer = await system_cache.get(key=rag_input.query)

        # print("\n\n".join(similar_documents))

        if not llm_answer:
            llm_answer = await self.llm_model.request(
                query=rag_input.query,
                documents="\n\n".join([x.text for x in similar_documents]),
                # prompt_template=rag_input.prompt_template
            )
            # llm_answer = 'abc xd'
            await system_cache.set(key=rag_input.query, val=llm_answer)

        print(llm_answer)

        return StrategyIn(
            query=rag_input.query,
            answer=str(llm_answer),
            documents=similar_documents,
            session_id=rag_input.session_id,
            debug_level=rag_input.debug_level,
            debug_info=rag_input.debug_info,
        )

    async def found_similar_docs(
        self, rag_input: EstimatorIn
    ) -> List[Document]:
        embedding = None
        if rag_input.search_strategy.is_use_embedding():
            embedding = self.vectorize_service.emb(rag_input.query)

        documents = await self.search_service[
            rag_input.search_strategy
        ].request(
            query=rag_input.query,
            num_docs=rag_input.num_docs,
            embedding=embedding,
        )
        # return [
        #     Document(
        #         text=item["_source"]["text_filtered"],
        #         title=item["_source"]["title3_main"],
        #         category=item["_source"]["title1"],
        #         similarity=item["_score"],
        #     )
        #     for item in documents
        # ]
        return documents
