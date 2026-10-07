from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: str = ''
    price: float = Field(..., ge=0)
    stock: int = Field(default=0, ge=0)
    category: str
    image_url: Optional[str] = None
    popularity_score: int = 0
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartItemPayload(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)


class CartItemRead(BaseModel):
    id: str
    product_id: str
    quantity: int
    product_name: str
    product_price: float
    image_url: Optional[str]


class OrderItemRead(BaseModel):
    id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


class OrderRead(BaseModel):
    id: str
    user_id: str
    total_amount: float
    payment_status: str
    order_status: str
    created_at: datetime
    items: List[OrderItemRead] = []


class PaymentRead(BaseModel):
    id: str
    order_id: str
    amount: float
    payment_method: str
    stripe_payment_id: Optional[str]
    status: str
    created_at: datetime


class NotificationRead(BaseModel):
    id: str
    user_id: str
    type: str
    message: str
    is_read: bool
    created_at: datetime


class UserProfile(BaseModel):
    id: str
    auth0_user_id: str
    name: str
    email: str
    role: str
