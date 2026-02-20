from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel,Field,field_validator
from app.utils.validators import validate_phone_number
from app.core.enums import Gender




class PatientBase(BaseModel):
    first_name: str = Field(...,min_length=1, max_length=100)
    last_name: str = Field(...,min_length=1, max_length=100)
    gender: Gender
    date_of_birth: date
    phone_number: str
    email: Optional[str] = None
    address: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        return validate_phone_number(v)



class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Gender
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        return validate_phone_number(v)


class PatientResponse(PatientBase):
    id: int
    mrn: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaginatedPatientResponse(BaseModel):
    total: int
    patients: List[PatientResponse]