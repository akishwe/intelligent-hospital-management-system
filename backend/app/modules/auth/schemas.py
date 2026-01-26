from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    role: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=64, description="Password must be between 6 and 64 characters long")


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

    