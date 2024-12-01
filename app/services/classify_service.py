from abc import ABC
from typing import List

from app.schemas.common.documents import Document
from app.schemas.common.estimators_dto import EstimatorIn, StrategyIn
from app.services.llm_providers import LlamaProvider
from app.services.redis.redis_service import NoCache, CacheRedis
from app.services.search_service import OpenSearchApiClient
from app.services.vectorization_service import TransformersVectorization
from app.utils.constants import CacheStrategy


class Rag(ABC):
    def __init__(self, redis_service):
        self.search_service = OpenSearchApiClient()
        self.vectorize_service = TransformersVectorization()
        self.llm_model = LlamaProvider()
        self.cache_system = {
            CacheStrategy.REDIS: CacheRedis(redis=redis_service),
            CacheStrategy.NO_CACHE: NoCache(),
        }

    async def get_answer(self, rag_input: EstimatorIn) -> StrategyIn:
        if (
                not rag_input.category.category
                and rag_input.intent_classifier.use
        ):
            pass # todo intent classifiactor returns user category: ex - rag_input.category.category = clf.returned_score

        similar_documents = await self.found_similar_docs(rag_input)

        # llm_answer = self.cache_holder.get(
        #     rag_input.text, rag_input.cache_strategy
        # )

        # debug_info = similar_documents.debug_info
        # if debug_info is None:
        #     debug_info = {}
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

        documents = await self.search_service.request(
            query=rag_input.query,
            num_docs=rag_input.num_docs,
            embedding=embedding
        )
        return [
            Document(
                text=item['_source']['text_filtered'],
                title=item['_source']['title3_main'],
                category=item['_source']['title1'],
                similarity=item['_score'],
            ) for item in documents
        ]





