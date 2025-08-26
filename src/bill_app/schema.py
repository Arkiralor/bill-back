import pytz

from pydantic import BaseModel, Field
from typing import List, Optional


class BillItemSchema(BaseModel):
    name: str
    description: str


class CreateBillSchema(BaseModel):
    customer_name: str
    customer_email: Optional[str]
    customer_address: str
    customer_phone: str
    items: Optional[List[BillItemSchema]]


class AddItemToBillSchema(BaseModel):
    items: List[BillItemSchema]


class CreateBillResponseSchema(BaseModel):
    id: str
    user: str
    customer_name: str
    customer_email: Optional[str]
    customer_address: str
    customer_phone: str
    items: Optional[List[BillItemSchema]]
    total_amount: float
    created_at: str
