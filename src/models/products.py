from beanie import Document
from pydantic import Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class Products(Document):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=500)
    price: float
    stock: int
    thumbnails: Optional[List[str]] = []  # URLs de Cloudinary
    category: List[str]

    model_config = {
        "arbitrary_types_allowed": True
    }

    class Settings:
        name = "products"
        bson_encoders = {ObjectId: str}
