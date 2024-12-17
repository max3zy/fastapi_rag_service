import re
import time
from typing import Any, Dict, Optional

# from da_robot_max_chain.da_log.logger import logger_factory
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from ollama import ChatResponse

from app.api.containers import AppContainer
from app.config import settings

# from app.da_log.events import LoggerEvents
# from app.da_log.logger import LogExtra
from app.preprocesses.preprocesses import preprocess
from app.schemas.rag import RagRequest, RagResponse
from app.services.answer_templates_storage import AnswerTemplateStorage
from app.services.classify_service import Rag
from app.services.llm_providers import LLamaClf, LLamaFewShot
from app.services.prompt_service import PromptService
from app.services.redis.redis_service import CacheRedis
from app.strategies.strategies import TrivialStrategy, create_answer
from app.utils.constants import StatusCode

router = APIRouter()

# logger = logger_factory(__name__)


@router.post(
    "/quest",
    response_model=RagResponse,
    response_model_exclude_none=True,
)
@inject
async def quest(
    request: RagRequest,
    rag: Rag = Depends(Provide[AppContainer.rag]),
    strategy: TrivialStrategy = Depends(
        Provide[AppContainer.trivial_strategy]
    ),
    prompt_storage: PromptService = Depends(
        Provide[AppContainer.prompt_storage]
    ),
    censor: LLamaFewShot = Depends(Provide[AppContainer.censor]),
    answers_storage: AnswerTemplateStorage = Depends(
        Provide[AppContainer.answer_storage]
    ),
) -> RagResponse:
    """
    workflow:
    1. preprocess request
    2. find documents -> summarize -> get llm answer (rag.get_answer method)
    3. postprocess answer
    """
    if request.censor.use:
        passed = await censor.request(request.query)
        if not passed:
            return RagResponse(
                answer=answers_storage.get(StatusCode.CENSORED),
                status_code=StatusCode.CENSORED,
                item_list=[],
            )

    estimator_input = preprocess(
        request=request, prompt_storage=prompt_storage
    )
    estimator_output = await rag.get_answer(rag_input=estimator_input)
    strategy_output = strategy.process(strategy_in=estimator_output)
    # logger.info(
    #     "Эндпоинт v1 сервиса успешно завершил свою работу",
    #     extra=LogExtra(
    #         query=query,
    #         is_use_score=is_use_score,
    #         threshold=threshold,
    #         response_time=time.time() - start_time,
    #         event=LoggerEvents.SERVICE_V1_SUCCESS,
    #     ).dict(),
    # )
    return create_answer(strategy_output=strategy_output)


@router.post("/flush")
@inject
async def flush(
    redis: CacheRedis = Depends(Provide[AppContainer.service_redis]),
):
    try:
        await redis.flush()
        answer = "FLUSHED"
    except Exception as e:
        answer = str(e)
    return answer


@router.get(
    "/classify_category",
    response_model=Dict[str, Any],
    response_model_exclude_none=True,
)
@inject
async def clf(
    text: str,
    classifier: LLamaClf = Depends(Provide[AppContainer.llama_clf]),
):
    """deprecated"""
    answer = await classifier.request(text)
    return {"answer": answer}
