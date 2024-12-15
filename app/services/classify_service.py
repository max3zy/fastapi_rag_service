from abc import ABC
from typing import Dict, List

from app.config import settings
from app.schemas.common.documents import Document
from app.schemas.common.estimators_dto import EstimatorIn, StrategyIn
from app.services.llm_providers import LlamaProvider
from app.services.redis.redis_service import CacheRedis, CacheSystem, NoCache
from app.services.search_service import (
    OpenSearchApiClient,
    OpenSearchFullTextApiClient,
    OpenSearchHybridApiClient,
    OpenSearchPrefixApiClient,
    OpenSearchVectorApiClient,
)
from app.services.vectorization_service import TransformersVectorization
from app.utils.constants import CacheStrategy, SearchStrategy


class Rag(ABC):
    def __init__(self, redis_service):
        self.search_service: Dict[SearchStrategy, OpenSearchApiClient] = {
            SearchStrategy.OPEN_SEARCH_VECTOR: OpenSearchVectorApiClient(
                index="gu_vector_faqs_v1",
            ),
            # SearchStrategy.OPEN_SEARCH_HYBRID: OpenSearchHybridApiClient(
            #     index="test_faqs_v1",
            # ),
            SearchStrategy.OPEN_SEARCH_FULL_TEXT: OpenSearchFullTextApiClient(
                index="gu_fulltext_faqs_v1",
            ),
            SearchStrategy.OPEN_SEARCH_PREFIX: OpenSearchPrefixApiClient(
                index="gu_prefix_faqs_v1",
            ),
        }
        self.vectorize_service = TransformersVectorization()
        self.llm_model = LlamaProvider()
        self.cache_system: Dict[CacheStrategy, CacheSystem] = {
            CacheStrategy.REDIS: CacheRedis(redis=redis_service),
            CacheStrategy.NO_CACHE: NoCache(),
        }

    async def get_answer(self, rag_input: EstimatorIn) -> StrategyIn:
        if not rag_input.category.category and rag_input.intent_classifier.use:
            pass  # todo intent classifiactor returns user category: ex - rag_input.category.category = clf.returned_score

        similar_documents = await self.found_similar_docs(rag_input)
        prompt_doc_template = "\n\n".join([x.text for x in similar_documents])

        system_cache = self.cache_system.get(
            rag_input.cache_strategy, CacheStrategy.NO_CACHE
        )
        llm_answer = await system_cache.get(
            key=rag_input.query + prompt_doc_template
        )

        if not llm_answer and rag_input.use_llm:
            llm_answer = await self.llm_model.request(
                query=rag_input.query,
                documents=prompt_doc_template,
                # prompt_template=rag_input.prompt_template
            )
            # llm_answer = 'abc xd'
            await system_cache.set(
                key=rag_input.query + prompt_doc_template, val=llm_answer
            )

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
            embedding = self.vectorize_service.emb(
                query=rag_input.query,
                vectorize_strategy=rag_input.vectorize_strategy,
            )

        documents = await self.search_service[
            rag_input.search_strategy
        ].request(
            query=rag_input.query,
            num_docs=rag_input.num_docs,
            embedding=embedding,
            category=rag_input.category.category,
        )

        return [
            doc
            for doc in sorted(documents)
            if doc.similarity > rag_input.sim_threshold
        ]
