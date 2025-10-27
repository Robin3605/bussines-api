from typing import List
from pydantic import BaseModel

class CartItemSchema(BaseModel):
    product_id: str
    quantity: int

class CartCreate(BaseModel):
    user_id: str

class AddItemRequest(BaseModel):
    product_id: str
    quantity: int

class CartResponse(BaseModel):
    id: str
    user_id: str
    items: List[CartItemSchema]

    class Config:
        orm_mode = True