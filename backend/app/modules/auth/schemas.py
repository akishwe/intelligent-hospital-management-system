from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator, root_validator
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

    model_config = ConfigDict(from_attributes=True)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        return validate_phone_number(v)

    @root_validator
    def check_age_and_role(cls, values):
        dob = values.get("date_of_birth")
        role = values.get("role")
        if dob:
            age = (datetime.today().date() - dob).days // 365
            if role in [UserRole.DOCTOR, UserRole.NURSE, UserRole.ADMIN] and age < 18:
                raise ValueError(f"{role} must be at least 18 years old")
        return values

    @root_validator
    def check_shift_times(cls, values):
        start = values.get("shift_start")
        end = values.get("shift_end")
        if start and end and end <= start:
            raise ValueError("shift_end must be after shift_start")
        return values

    @root_validator
    def role_required_fields(cls, values):
        role = values.get("role")
        if role == UserRole.DOCTOR and not values.get("specialization"):
            raise ValueError("Doctor must have a specialization")
        if role in [UserRole.DOCTOR, UserRole.NURSE] and not values.get("qualification"):
            raise ValueError(f"{role} must have a qualification")
        return values


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=64)


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
    def validate_phone(cls, v):
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


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserInfo