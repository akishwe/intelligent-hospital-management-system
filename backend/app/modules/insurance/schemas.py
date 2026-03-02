from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import date
from enum import Enum


class CoverageType(str, Enum):
    HMO = "HMO"
    PPO = "PPO"
    EPO = "EPO"
    POS = "POS"
    INTERNATIONAL = "International"
    OTHER = "Other"


class InsuranceBase(BaseModel):
    provider_name: str = Field(..., max_length=100)
    provider_code: Optional[str] = Field(None, max_length=50)
    policy_number: str = Field(..., max_length=50)
    coverage_type: Optional[CoverageType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: Optional[bool] = True
    coverage_limit: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    external_reference: Optional[str] = Field(None, max_length=100)

    model_config = {"from_attributes": True}

    @field_validator("provider_name", "policy_number")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Must not be empty")
        return v.strip()

    @field_validator("currency")
    def validate_currency(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")
        return v.upper() if v else v

    @field_validator("coverage_limit")
    def validate_coverage_limit(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Coverage limit must be positive")
        return v

    @model_validator(mode="before")
    def check_dates(cls, values: dict) -> dict:
        start, end = values.get("start_date"), values.get("end_date")
        if start and end and start > end:
            raise ValueError("Start date cannot be after end date")
        return values


class InsuranceCreate(InsuranceBase):
    patient_id: int = Field(..., description="ID of the patient this insurance belongs to")


class InsuranceUpdate(BaseModel):
    provider_name: Optional[str] = Field(None, max_length=100)
    provider_code: Optional[str] = Field(None, max_length=50)
    policy_number: Optional[str] = Field(None, max_length=50)
    coverage_type: Optional[CoverageType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: Optional[bool] = None
    coverage_limit: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    external_reference: Optional[str] = Field(None, max_length=100)

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    def check_update_dates(cls, values: dict) -> dict:
        start, end = values.get("start_date"), values.get("end_date")
        if start and end and start > end:
            raise ValueError("Start date cannot be after end date")
        return values


class InsuranceResponse(InsuranceBase):
    id: int
    patient_id: int