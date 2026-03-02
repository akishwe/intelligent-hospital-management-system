from pydantic import BaseModel, Field
from typing import Optional

class QualificationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

    model_config = {
        "from_attributes": True
    }

class QualificationCreate(QualificationBase):
    pass

class QualificationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)

    model_config = {
        "from_attributes": True
    }

class QualificationResponse(QualificationBase):
    id: int