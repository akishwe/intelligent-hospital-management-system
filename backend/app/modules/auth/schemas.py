from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from datetime import date
from app.utils.validators import validate_phone_number
from app.core.enums import UserRole, Gender

class UserInfo(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    role: UserRole
    is_active: bool
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    department: Optional[str] = None
    notes: Optional[str] = None
    failed_attempts: int
    account_locked_until: Optional[date] = None
    is_superuser: bool
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    role: UserRole
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    department: Optional[str] = None
    notes: Optional[str] = None
    is_superuser: Optional[bool] = False

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        return validate_phone_number(v)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=64, description="Password must be between 6 and 64 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    failed_attempts: int
    account_locked_until: Optional[date] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo