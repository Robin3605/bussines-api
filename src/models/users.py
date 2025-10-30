from beanie import Document, Link
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from bson import ObjectId
from src.models.cart import Cart
from beanie import PydanticObjectId

class RoleEnum(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    DELIVERY = "delivery"

class Users(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: Optional[str]
    google_id: Optional[str] = None
    role: RoleEnum = RoleEnum.CLIENT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cart_id: Optional[PydanticObjectId] = None

    model_config = {
        "arbitrary_types_allowed": True
        
    }

    class Settings:
        name = "users"
        bson_encoders = {
            ObjectId: str  # Convierte ObjectId a string automáticamente
        }

    async def create_cart(self):
        """Crea un carrito automáticamente cuando se registra el usuario"""
        # from src.models.carts import Cart
        # cart = Cart(user_id=self.id, items=[])
        cart = Cart(user_id=self.id)
        await cart.insert()
        self.cart_id = cart.id
        await self.save()