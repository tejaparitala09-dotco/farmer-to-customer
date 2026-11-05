"""Pydantic models used by the API and MongoDB user documents."""

from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, EmailStr, Field

UserRole = Literal["customer", "farmer"]


class RegistrationRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(min_length=7, max_length=25)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserDocument(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone_number: str
    password_hash: str
    role: UserRole


class CustomerDocument(UserDocument):
    role: Literal["customer"] = "customer"


class FarmerDocument(UserDocument):
    role: Literal["farmer"] = "farmer"


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone_number: str
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


ProductCategory = Literal["Vegetables", "Fruits", "Grains", "Dairy", "Other"]
OrderStatus = Literal["Pending", "Confirmed", "Shipped", "Out for Delivery", "Delivered", "Cancelled", "Preparing"]


class ProductCreate(BaseModel):
    product_name: str = Field(min_length=2, max_length=120)
    category: ProductCategory
    price: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=30)
    quantity: float = Field(gt=0)
    description: str = Field(default="", max_length=1000)
    image_url: str = Field(default="", max_length=500)


class ProductResponse(ProductCreate):
    id: str
    farmer_id: str
    farmer_name: str
    created_at: datetime
    updated_at: datetime


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: float = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(min_length=1)
    delivery_address: str = Field(min_length=5, max_length=300)


class OrderItemResponse(BaseModel):
    product_id: str
    farmer_id: str
    farmer_name: str
    product_name: str
    unit: str
    price: float
    quantity: float
    line_total: float


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    customer_name: str
    farmer_ids: List[str]
    items: List[OrderItemResponse]
    total_amount: float
    delivery_address: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
