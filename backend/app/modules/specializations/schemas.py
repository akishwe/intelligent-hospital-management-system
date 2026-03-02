from pydantic import BaseModel, Field
from typing import Optional

class SpecializationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

    model_config = {
        "from_attributes": True
    }

class SpecializationCreate(SpecializationBase):
    pass

class SpecializationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)

    model_config = {
        "from_attributes": True
    }

class SpecializationResponse(SpecializationBase):
    id: int