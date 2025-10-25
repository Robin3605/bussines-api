from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.models.users import RoleEnum
from bson import ObjectId

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str]
    google_id: Optional[str] = None

class UserUpdate(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    role: RoleEnum
    cart_id: Optional[str] = None
    created_at: datetime

    # model_config = {
    #     "populate_by_name": True
    # }

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class User_login(BaseModel):
    email: str
    password: str

    # class Config:
    #     populate_by_name = True