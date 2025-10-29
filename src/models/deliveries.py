from beanie import Document
from pydantic import EmailStr
from typing import Optional
from datetime import datetime



class Delivery(Document):
    order_id: str
    deliver_name: str
    # address: str
    tracking_number: Optional[str]
    status: str = "preparing"  # preparing, in_transit, delivered
    estimated_date: Optional[datetime]