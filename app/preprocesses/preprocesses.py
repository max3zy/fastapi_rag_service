from app.schemas.common.estimators_dto import EstimatorIn
from app.services.prompt_service import PromptService
from app.utils.preprocess.preprocessing import text_cleanup_preprocessor, \
    clean_html

from app.schemas.rag import RagRequest


def preprocess(
    request: RagRequest, prompt_storage: PromptService
) -> EstimatorIn:
    cleanup_text = text_cleanup_preprocessor(
        clean_html(request.query)
    )
    system_prompt = prompt_storage.get(request.prompt_type)
    return EstimatorIn(
        query=cleanup_text,
        num_docs=request.num_docs,
        search_strategy=request.search_strategy,
        cache_strategy=request.cache_strategy,
        category=request.category,
        intent_classifier=request.intent_classifier,
        session_id=request.session_id,
        system_prompt=system_prompt,
        debug_level=request.debug_level,
        debug_info=(
            {"original_query": request.query}
            if request.debug_level.is_high_level() else None
        )
    )
