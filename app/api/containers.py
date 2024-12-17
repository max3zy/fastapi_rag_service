from dependency_injector import containers, providers

from app.config import settings
from app.services.answer_templates_storage import AnswerTemplateStorage

from app.services.classify_service import Rag
from app.services.llm_providers import LLamaFewShot, LLamaClf
from app.services.prompt_service import PromptService
from app.services.redis.redis_init_pool import init_redis_pool
from app.services.redis.redis_service import CacheRedis
from app.strategies.strategies import TrivialStrategy


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(
        {
            "path_to_models": settings.PATH_TO_MODELS,
            "classifier_onnx_model": settings.CLASSIFIER_ONNX_MODEL,
            "redis_host": settings.CACHE_HOST_REDIS,
            "redis_port": settings.CACHE_PORT_REDIS,
        }
    )

    redis_pool = providers.Resource(
        init_redis_pool,
        host=config.redis_host,
        port=config.redis_port,
    )

    service_redis = providers.Singleton(
        CacheRedis,
        redis=redis_pool,
    )

    # llama_clf = providers.Singleton(LLamaClf)

    censor = providers.Singleton(LLamaFewShot)

    answer_storage = providers.Singleton(AnswerTemplateStorage)

    rag = providers.Singleton(
        Rag,
        redis_service=service_redis,
    )

    prompt_storage = providers.Singleton(PromptService)

    trivial_strategy = providers.Singleton(TrivialStrategy)
