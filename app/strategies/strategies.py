from abc import ABC, abstractmethod

from app.schemas.common.estimators_dto import StrategyIn, StrategyOut
from app.schemas.rag import RagResponse
from app.utils.constants import StatusCode
from app.utils.preprocess.preprocessing import answer_postprocessing


class AbstractStrategyPrediction(ABC):
    @abstractmethod
    def process(self, strategy_in: StrategyIn) -> StrategyOut:
        pass


class TrivialStrategy(AbstractStrategyPrediction):
    def process(self, strategy_in: StrategyIn) -> StrategyOut:
        answer = answer_postprocessing(str(strategy_in.answer))
        return StrategyOut(
            answer=answer,
            documents=strategy_in.documents,
            session_id=strategy_in.session_id,
            debug_level=strategy_in.debug_level,
            debug_info=strategy_in.debug_info,
        )


def create_answer(strategy_output: StrategyOut) -> RagResponse:
    return RagResponse(
        answer=strategy_output.answer,
        item_list=strategy_output.documents,
        debug_info=strategy_output.debug_info,
        status_code=StatusCode.PASSED,
    )
