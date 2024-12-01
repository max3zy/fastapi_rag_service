from abc import ABC, abstractmethod

from app.schemas.classify import ClassifyResponse
from app.schemas.common.estimators_dto import StrategyIn, StrategyOut
from app.schemas.rag import RagResponse


class AbstractStrategyPrediction(ABC):
    @abstractmethod
    def process(self, strategy_in: StrategyIn) -> StrategyOut:
        pass


class TrivialStrategy(AbstractStrategyPrediction):
    def process(self, strategy_in: StrategyIn) -> StrategyOut:
        # todo POST_PROCESSING PART
        return StrategyOut(
            answer=strategy_in.answer,
            documents=strategy_in.documents,
            session_id=strategy_in.session_id,
            debug_level=strategy_in.debug_level,
            debug_info=strategy_in.debug_info,
        )



def create_answer(strategy_output: StrategyOut) -> RagResponse:
    return RagResponse(
        answer=strategy_output.answer,
        item_list=strategy_output.documents,
        debug_info=strategy_output.debug_info
    )
