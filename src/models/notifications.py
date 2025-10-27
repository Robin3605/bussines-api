from beanie import Document
from pydantic import  Field
from typing import Optional
from datetime import datetime



class Notification(Document):
    user_id: str
    message: str
    type: str  # order_update, payment_success, etc.
    read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)