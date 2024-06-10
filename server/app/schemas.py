from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from server.app.models import OrderStatus


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    disabled: Optional[bool] = None


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: UUID


class CustomerBase(BaseModel):
    name: str
    address: str
    username: Optional[str] = None


class CustomerCreate(CustomerBase):
    hash: str


class CustomerRead(CustomerBase):
    id: UUID
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    price: float
    quantity_in_stock: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: UUID

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    product_id: UUID
    quantity: int = 1


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: UUID
    customer_id: UUID
    status: OrderStatus
    order_date: datetime
    product: ProductRead

    class Config:
        orm_mode = True
