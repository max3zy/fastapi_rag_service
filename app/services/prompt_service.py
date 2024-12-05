from app.utils.constants import PromptType


class PromptService:
    def __init__(self):
        self.prompt_storage = {PromptType.DEFAULT: "default prompt ..."}

    def get(self, prompt_type: PromptType) -> str:
        """
        выбирается промпт по ключу в зависимости от значения, передаваемого в запросе
        """
        return self.prompt_storage.get(prompt_type)
