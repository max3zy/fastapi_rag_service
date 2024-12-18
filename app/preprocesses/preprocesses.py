from app.schemas.common.estimators_dto import EstimatorIn
from app.schemas.rag import RagRequest
from app.services.prompt_service import PromptService
from app.utils.preprocess.preprocessing import (
    clean_html,
    text_cleanup_preprocessor,
)


def preprocess(
    request: RagRequest, prompt_storage: PromptService
) -> EstimatorIn:
    cleanup_text = text_cleanup_preprocessor(clean_html(request.query))
    system_prompt = prompt_storage.get(request.prompt_type)  # deprecated
    return EstimatorIn(
        query=cleanup_text,
        num_docs=request.num_docs,
        search_strategy=request.search_strategy,
        cache_strategy=request.cache_strategy,
        category=request.category,
        intent_classifier=request.intent_classifier,
        session_id=request.session_id,
        system_prompt=system_prompt,
        sim_threshold=request.sim_threshold,
        vectorize_strategy=request.vectorize_strategy,
        use_llm=request.use_llm,
        debug_level=request.debug_level,
        debug_info=(
            {"original_query": request.query}
            if request.debug_level.is_high_level()
            else None
        ),
    )
