import random
from typing import Dict, List, Optional

from app.utils.constants import StatusCode


class AnswerTemplateStorage:
    def __init__(self):
        self.storage: Dict[StatusCode, List[str]] = {
            StatusCode.CENSORED: [
                "Не могу помочь с этим вопросом",
                "Понял Вас, но не нашел, что ответить",
                "Я не готов обсуждать эту тему",
                "Не готов ответить на Ваш вопрос. Спросите что-нибудь еще",
            ],
            StatusCode.NO_ANSWER: [
                "Не нашел, что ответить на Ваш вопрос",
                "Изучил информацию, но пока не могу ответить на Ваш вопрос",
                "Попробуйте задать вопрос иначе",
            ],
        }

    def get(self, status: StatusCode, answer: Optional[str] = None) -> str:
        if status in self.storage.keys():
            return random.choice(self.storage.get(status))
        else:
            return answer
