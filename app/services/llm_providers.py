import re
from abc import ABC, abstractmethod
from typing import Union

from ollama import ChatResponse, Client, GenerateResponse

from app.utils.base_model import singleton
from app.utils.preprocess.preprocessing import (
    clean_html,
    text_cleanup_preprocessor,
)


class Llama(ABC):
    LLAMA_HOST = "127.0.0.1:11434"
    MODEL = "llama3.2"

    def __init__(self):
        self.model = Client(host=self.LLAMA_HOST)

    @abstractmethod
    async def request(self, query, documents) -> Union[str, bool]:
        pass

    @abstractmethod
    def process_response(self, response: ChatResponse) -> Union[str, bool]:
        pass


class LLamaFewShot(Llama):
    PROMPT_TEMPLATE = """ 
    Твоя задача - классифицировать текст как вредоносный или безопасный.
    Текст: ```{query}``. 
    Дай ответ одним словом - Вредоносный или Безопасный
    """
    SECURE_PATTERN = r"безопас"

    def __init__(self):
        super().__init__()

    async def request(self, query, documents=None) -> bool:
        response = self.model.chat(
            model=self.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": self.PROMPT_TEMPLATE.format(
                        query=text_cleanup_preprocessor(clean_html(query))
                    ),
                }
            ],
        )
        return self.process_response(response)

    def process_response(self, response: ChatResponse) -> bool:
        return bool(
            re.search(
                self.SECURE_PATTERN, response.message.content, re.IGNORECASE
            )
        )


@singleton
class LlamaProvider(Llama):
    # PROMPT_TEMPLATE = """
    # Роль: энциклопедия.
    # Цель: максимально точно ответить на вопрос при использовании контекста.
    # Необходимо найти в контексте информацию по вопросу и на основании этой информации сформулировать ответ.
    # Если в контексте нет информации по вопросу, то отвечай "В моей базе знаний нет информации по данному вопросу".
    # Твой ответ должен основываться исключительно на фактах, предоставленных в контексте.
    # Дополнительный текст: выводить запрещено.
    # Стиль: деловой.
    # Орфография: исправлять.
    # Отвечать обязательно строго на русском языке и строго на вопрос.
    # Ответ писать строго в формате МАРКДАУН.
    # ВОПРОС: ```{query}```.
    # Контекст: ```{documents}```
    # """

    PROMPT_TEMPLATE = """ 
    Роль: энциклопедия.
    Твоя задача максимально точно ответить на вопрос пользователя на основании предоставленной информации.
    Отвечай строго на русском, не придумывай факты, которых нет в тексте. 
    Ответ должен быть строго в формате маркдаун.
    ВОПРОС: ```{query}```. 
    Информация: ```{documents}```
    """

    def __init__(self):
        super().__init__()

    async def request(self, query: str, documents: str) -> str:
        response = self.model.chat(
            model=self.MODEL,
            messages=[
                {"role": "user", "content": self.make_prompt(query, documents)}
            ],
            options={"num_ctx": 200},
        )
        return self.process_response(response)

    def process_response(self, response: ChatResponse) -> str:
        return response.message.content

    def make_prompt(self, query: str, documents: str) -> str:
        return self.PROMPT_TEMPLATE.format(
            query=query,
            documents=documents,
        )


class LLamaClf(Llama):
    PROMPT_TEMPLATE = """
    Твоя задача - помочь пользователю определиться с категорией его запроса.
    Всего существует 6 категорий: "Социальная поддержка", "Транспорт", "Финансы, налоги, штрафы", "Образование", "Личные документы", "Другое"

    Запрос пользователя: ```{text}```
    Нужно в ответе написать ровно одну категорию из предоставленного выше списка. Ни словом больше ни словом меньше.
    Запрос представляет из себя обращение на портал Госуслуги поэтому нужно максимально точно определить категорию.
    """
    SECURE_PATTERN = r"безопас"

    def __init__(self):
        super().__init__()

    async def request(self, query, documents=None) -> str:
        response = self.model.generate(
            model=self.MODEL,
            prompt=self.PROMPT_TEMPLATE.format(
                text=text_cleanup_preprocessor(clean_html(query))
            ),
        )
        return self.process_response(response)

    def process_response(self, response: GenerateResponse) -> str:
        return response.response
