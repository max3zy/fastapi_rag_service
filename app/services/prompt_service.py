from app.utils.constants import PromptType


class PromptService:
    def __init__(self):
        self.prompt_storage = {PromptType.DEFAULT: "default prompt ..."}

    def get(self, prompt_type: PromptType) -> str:
        return self.prompt_storage.get(prompt_type)
