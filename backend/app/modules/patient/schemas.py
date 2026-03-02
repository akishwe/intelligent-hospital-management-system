from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import date, datetime
from app.utils.validators import validate_phone_number
from app.core.enums import Gender, BloodGroup, MaritalStatus

class PatientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    gender: Gender
    date_of_birth: date
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = "India"
    national_id: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_valid_till: Optional[date] = None
    insurance_type: Optional[str] = None
    billing_account_number: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    current_medications: Optional[str] = None
    past_surgeries: Optional[str] = None
    immunization_history: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    organ_donor: Optional[bool] = False
    marital_status: Optional[MaritalStatus] = None
    language: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    religion: Optional[str] = None
    occupation: Optional[str] = None
    notes: Optional[str] = None
    photo: Optional[str] = None
    preferred_pharmacy: Optional[str] = None
    preferred_doctor_id: Optional[int] = None
    primary_physician_id: Optional[int] = None
    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    ward: Optional[str] = None
    room_number: Optional[str] = None
    bed_number: Optional[str] = None
    consent_signed: Optional[bool] = False
    consent_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_relation: Optional[str] = None
    last_visit_date: Optional[date] = None
    created_by_staff_id: Optional[int] = None
    updated_by_staff_id: Optional[int] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        return validate_phone_number(v)

    @field_validator("emergency_contact_phone")
    @classmethod
    def validate_emergency_phone(cls, v):
        if v:
            return validate_phone_number(v)
        return v


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    national_id: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_valid_till: Optional[date] = None
    insurance_type: Optional[str] = None
    billing_account_number: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    current_medications: Optional[str] = None
    past_surgeries: Optional[str] = None
    immunization_history: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    organ_donor: Optional[bool] = None
    marital_status: Optional[MaritalStatus] = None
    language: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    religion: Optional[str] = None
    occupation: Optional[str] = None
    notes: Optional[str] = None
    photo: Optional[str] = None
    preferred_pharmacy: Optional[str] = None
    preferred_doctor_id: Optional[int] = None
    primary_physician_id: Optional[int] = None
    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    ward: Optional[str] = None
    room_number: Optional[str] = None
    bed_number: Optional[str] = None
    consent_signed: Optional[bool] = None
    consent_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_relation: Optional[str] = None
    last_visit_date: Optional[date] = None
    created_by_staff_id: Optional[int] = None
    updated_by_staff_id: Optional[int] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v:
            return validate_phone_number(v)
        return v

    @field_validator("emergency_contact_phone")
    @classmethod
    def validate_emergency_phone(cls, v):
        if v:
            return validate_phone_number(v)
        return v


class PatientResponse(PatientBase):
    id: int
    mrn: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class PaginatedPatientResponse(BaseModel):
    total: int
    patients: List[PatientResponse]