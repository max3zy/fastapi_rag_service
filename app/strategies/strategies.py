from abc import ABC, abstractmethod

from app.schemas.common.estimators_dto import StrategyIn, StrategyOut
from app.schemas.rag import RagResponse
from app.utils.constants import NO_ANSWER, StatusCode
from app.utils.preprocess.preprocessing import answer_postprocessing


class AbstractStrategyPrediction(ABC):
    @abstractmethod
    def process(self, strategy_in: StrategyIn) -> StrategyOut:
        pass


class TrivialStrategy(AbstractStrategyPrediction):
    def process(self, strategy_in: StrategyIn) -> StrategyOut:
        answer = answer_postprocessing(str(strategy_in.answer))
        status_code = (
            StatusCode.NO_ANSWER if answer in NO_ANSWER else StatusCode.PASSED
        )
        return StrategyOut(
            answer=answer,
            documents=strategy_in.documents,
            session_id=strategy_in.session_id,
            debug_level=strategy_in.debug_level,
            debug_info=strategy_in.debug_info,
            status_code=status_code,
        )


def create_answer(strategy_output: StrategyOut) -> RagResponse:
    return RagResponse(
        answer=strategy_output.answer,
        item_list=strategy_output.documents,
        debug_info=strategy_output.debug_info,
        status_code=strategy_output.status_code,
    )
