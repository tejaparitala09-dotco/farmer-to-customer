from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    phone: Optional[str] = Field(default="", max_length=25)
    role: str = "customer"

    @field_validator("role")
    @classmethod
    def valid_role(cls, value: str):
        cleaned = value.lower().strip()
        if cleaned not in {"customer", "farmer"}:
            raise ValueError("Role must be customer or farmer")
        return cleaned

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class ProductRequest(BaseModel):
    product_name: str = Field(min_length=2, max_length=100)
    category: str = Field(default="Vegetables")
    price: float = Field(gt=0)
    unit: str = Field(default="kg")
    quantity: float = Field(ge=0)
    description: str = Field(min_length=2)
    image_url: Optional[str] = Field(default="")

class OrderItem(BaseModel):
    product_id: str
    quantity: float = Field(gt=0)

class Address(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str = Field(min_length=6)
    address: str = Field(min_length=3)
    city: str = Field(min_length=2)
    state: str = Field(min_length=2)
    pincode: str = Field(min_length=3)

class CreateOrderRequest(BaseModel):
    items: List[OrderItem] = Field(min_length=1)
    delivery_address: Address

class StatusRequest(BaseModel):
    status: str
