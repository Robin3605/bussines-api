from beanie import Document
from pydantic import Field, BaseModel
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId

class CartItem(BaseModel):
    product_id: PydanticObjectId
    quantity: int = Field(default=1, ge=1)  # 👈 mínimo 1


class Cart(Document):
    user_id: Optional[PydanticObjectId] = None
    items: List[CartItem] = Field(default_factory=list)  # 👈 usa la clase CartItem, no dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "arbitrary_types_allowed": True
    }

    class Settings:
        name = "carts"
        bson_encoders = {
            ObjectId: str  # Convierte ObjectId a string automáticamente
        }