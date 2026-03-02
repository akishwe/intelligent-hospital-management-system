from pydantic import BaseModel, Field, field_validator
from typing import Optional

class HospitalBase(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    country: str = Field(..., max_length=100)
    is_active: Optional[bool] = True

    model_config = {"from_attributes": True}

    @field_validator("name", "code", "country")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Must not be empty")
        return v.strip()


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

    model_config = {"from_attributes": True}

    @field_validator("name", "code", "country")
    def not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Must not be empty")
        return v.strip()


class HospitalResponse(HospitalBase):
    id: int