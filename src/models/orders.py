from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime
from src.models.cart import  CartItem


class Order(Document):
    user_id: str
    items: List[CartItem]
    total: float
    status: str = "pending"  # pending, paid, shipped, delivered, canceled
    # payment_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)