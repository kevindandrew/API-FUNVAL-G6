from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: Decimal
    status: str
    created_at: datetime
    user_name: Optional[str] = None # Para mostrar nombre en listas de admin
    
    class Config:
        from_attributes = True

class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse]

class OrderStatusUpdate(BaseModel):
    status: str
