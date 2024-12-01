from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
