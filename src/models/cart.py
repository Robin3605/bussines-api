from beanie import Document
from pydantic import Field
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

class CartItem(BaseException):
    product_id: str
    quantity: int = 1

class Cart(Document):
    user_id: ObjectId
    items: List[dict] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "arbitrary_types_allowed": True
    }

    class Settings:
        name = "carts"