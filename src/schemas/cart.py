from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class CartItemSchema(BaseModel):
    product_id: str
    quantity: int

class CartCreate(BaseModel):
    user_id: str

class AddItemRequest(BaseModel):
    product_id: str
    quantity: int

class CartResponse(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    items: List[CartItemSchema] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

    # class Config:
    #     populate_by_name = True
    #     from_attributes = True