from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ConfigDict
from datetime import date, datetime
from app.utils.validators import validate_phone_number
from app.core.enums import Gender, BloodGroup, MaritalStatus, AllergySeverity

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

    @field_validator("height_cm")
    @classmethod
    def validate_height(cls, v):
        if v is not None and (v <= 0 or v > 300):
            raise ValueError("Height must be between 1 and 300 cm")
        return v

    @field_validator("weight_kg")
    @classmethod
    def validate_weight(cls, v):
        if v is not None and (v <= 0 or v > 500):
            raise ValueError("Weight must be between 1 and 500 kg")
        return v

    @model_validator(mode="after")
    def validate_business_rules(self):
        if self.date_of_birth > date.today():
            raise ValueError("Date of birth cannot be in the future")
        if self.insurance_valid_till and self.insurance_valid_till < date.today():
            raise ValueError("Insurance validity cannot be in the past")
        if self.admission_date and self.discharge_date:
            if self.discharge_date < self.admission_date:
                raise ValueError("Discharge date cannot be before admission date")
        if self.consent_signed and not self.consent_date:
            raise ValueError("Consent date required if consent is signed")
        if self.consent_date and not self.consent_signed:
            raise ValueError("Consent must be signed if consent date is provided")
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            self.bmi = round(self.weight_kg / (height_m ** 2), 2)
        return self


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None

    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    consent_signed: Optional[bool] = None
    consent_date: Optional[date] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v:
            return validate_phone_number(v)
        return v

    @model_validator(mode="after")
    def validate_update_rules(self):
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValueError("Date of birth cannot be in the future")
        if self.admission_date and self.discharge_date:
            if self.discharge_date < self.admission_date:
                raise ValueError("Discharge date cannot be before admission date")
        return self


class PatientResponse(PatientBase):
    id: int
    mrn: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class PaginatedPatientResponse(BaseModel):
    total: int
    patients: List[PatientResponse]

class AllergyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    severity: Optional[AllergySeverity] = None
    reaction: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Allergy name cannot be empty")
        return v.title()

    @field_validator("reaction", "notes")
    @classmethod
    def validate_optional_strings(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v if v else None