import re
from abc import ABC, abstractmethod
from typing import Any, List, Union

from ollama import AsyncClient, ChatResponse, Client, GenerateResponse

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


class LlamaProvider(Llama):
    PROMPT_TEMPLATE = """ 
    ТЫ - умный помощник портала госуслуги. 
    Твоя задача дать максимально точный ответ на вопрос пользователя 
    на основании информации из предоставленных документов. 
    НЕ ПРИДУМЫВАЙ ничего от себя, отвечай только исходя из контекста документов.
    ВОПРОС ПОЛЬЗОВАТЕЛЯ: ```{query}```. ДОКУМЕНТЫ: ```{documents}```
    """

    def __init__(self):
        super().__init__()

    async def request(self, query: str, documents: str) -> str:
        response = self.model.chat(
            model=self.MODEL,
            messages=[
                {"role": "user", "content": self.make_prompt(query, documents)}
            ],
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
            )
        )
        return self.process_response(response)

    def process_response(self, response: GenerateResponse) -> str:
        return response.response