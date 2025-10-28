from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class Products(Document):
    # id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=500)
    price: float
    stock: int
    thumbnails: Optional[List[str]] = []  # URLs de Cloudinary
    category: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "arbitrary_types_allowed": True
    }

    class Settings:
        name = "products"
        bson_encoders = {ObjectId: str}
