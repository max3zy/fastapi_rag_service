from typing import Optional

from pydantic import BaseModel


class Censor(BaseModel):
    use: bool = False
    type: Optional[str] = "default_censor"
    threshold: float = 0.0
