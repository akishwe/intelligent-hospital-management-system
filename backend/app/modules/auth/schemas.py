from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from datetime import date, datetime, time
from app.utils.validators import validate_phone_number
from app.core.enums import UserRole, Gender

class UserInfo(BaseModel):
    id: int
    staff_id: Optional[str] = None
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
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    shift_start: Optional[time] = None
    shift_end: Optional[time] = None
    last_login: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
    two_factor_enabled: bool = False
    hospital_id: Optional[str] = None
    failed_attempts: int
    account_locked_until: Optional[datetime] = None
    is_superuser: bool
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    staff_id: Optional[str] = None
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
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    shift_start: Optional[time] = None
    shift_end: Optional[time] = None
    two_factor_enabled: bool = False
    hospital_id: Optional[str] = None
    is_superuser: Optional[bool] = False

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        return validate_phone_number(v)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=64, description="Password must be between 6 and 64 characters long")


class UserUpdate(BaseModel):
    staff_id: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[UserRole] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    department: Optional[str] = None
    notes: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    shift_start: Optional[time] = None
    shift_end: Optional[time] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    failed_attempts: Optional[int] = None
    account_locked_until: Optional[datetime] = None
    last_login: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
    two_factor_enabled: Optional[bool] = None
    hospital_id: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if v is None:
            return v
        return validate_phone_number(v)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    failed_attempts: int
    account_locked_until: Optional[datetime] = None
    last_login: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo