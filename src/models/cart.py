from beanie import Document
from pydantic import Field, BaseModel
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

class CartItem(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)  # 👈 mínimo 1


class Cart(Document):
    user_id: ObjectId
    items: List[CartItem] = []  # 👈 usa la clase CartItem, no dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "arbitrary_types_allowed": True
    }

    class Settings:
        name = "carts"