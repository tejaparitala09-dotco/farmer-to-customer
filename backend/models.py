from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    phone: str = Field(default="", max_length=20)
    role: str
    @field_validator("role")
    @classmethod
    def valid_role(cls, value):
        if value not in {"customer", "farmer"}: raise ValueError("Role must be customer or farmer")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ProductRequest(BaseModel):
    product_name: str = Field(min_length=2, max_length=100)
    category: str
    price: float = Field(gt=0)
    unit: str
    quantity: float = Field(gt=0)
    description: str = Field(min_length=5)
    image_url: Optional[str] = ""

class OrderItem(BaseModel):
    product_id: str
    quantity: float = Field(gt=0)

class Address(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str = Field(min_length=7)
    address: str = Field(min_length=3)
    city: str = Field(min_length=2)
    state: str = Field(min_length=2)
    pincode: str = Field(min_length=4)

class CreateOrderRequest(BaseModel):
    items: List[OrderItem] = Field(min_length=1)
    delivery_address: Address

class StatusRequest(BaseModel):
    status: str
