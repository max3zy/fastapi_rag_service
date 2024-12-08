import random
from typing import Dict, List

from app.utils.constants import StatusCode


class AnswerTemplateStorage:
    def __init__(self):
        self.storage: Dict[StatusCode, List[str]] = {
            StatusCode.CENSORED: [
                "Не могу помочь с этим вопросом",
                "Понял Вас, но не нашел, что ответить",
                "Я не готов обсуждать эту тему",
                "Не готов ответить на Ваш вопрос. Спросите что-нибудь еще",
            ]
        }

    def get(self, status: StatusCode) -> str:
        if status in self.storage.keys():
            return random.choice(self.storage.get(status))
