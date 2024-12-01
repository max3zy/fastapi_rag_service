from typing import List, Any

from ollama import Client, AsyncClient


class LlamaProvider:
    LLAMA_HOST = '127.0.0.1:11434'
    MODEL = 'llama3.2'
    PROMPT_TEMPLATE = """ 
    ТЫ - умный помощник портала госуслуги. 
    Твоя задача дать максимально точный ответ на вопрос пользователя 
    на основании информации из предоставленных документов. 
    НЕ ПРИДУМЫВАЙ ничего от себя, отвечай только исходя из контекста документов.
    ВОПРОС ПОЛЬЗОВАТЕЛЯ: ```{query}```. ДОКУМЕНТЫ: ```{documents}```
    """

    def __init__(self):
        self.model = Client(host=self.LLAMA_HOST)

    async def request(self, query: str, documents: str) -> str:
        return self.model.chat(
            model=self.MODEL,
            messages=[
                {
                    'role': 'user',
                    'content': self.make_prompt(query, documents)
                }
            ]
        )

    def make_prompt(self, query: str, documents: str):
        print(self.PROMPT_TEMPLATE.format(
            query=query,
            documents=documents,
        ))
        return self.PROMPT_TEMPLATE.format(
            query=query,
            documents=documents,
        )