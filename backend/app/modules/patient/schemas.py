from datetime import date
from typing import Optional
from pydantic import BaseModel,Field


class PatientBase(BaseModel):
    first_name: str = Field(...,min_length=1, max_length=100)
    last_name: str = Field(...,min_length=1, max_length=100)
    gender: str = Field(...,description="Male/Female/Other")
    date_of_birth: date
    phone_number: str = Field(...,min_length=10, max_length=15)
    email: Optional[str] = None
    address: Optional[str] = None


class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class PatientResponse(PatientBase):
    id: int
    created_at: Optional[date] = None
    updated_at: Optional[date] = None

    class Config:
        from_attributes = True