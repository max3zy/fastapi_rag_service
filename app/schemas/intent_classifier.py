from pydantic import BaseModel


class IntentClf(BaseModel):
    use: bool = False
    type: str = "default_intent_clf"
    threshold: float = 0.
