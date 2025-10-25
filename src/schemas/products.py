from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    category: List[str]
    # thumbnails: Optional[List[str]] = []

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[List[str]] = None
    # thumbnails: Optional[List[str]]  = None

class ProductResponse(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    price: float
    stock: int
    category: List[str]
    thumbnails: Optional[List[str]] = []
    created_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
