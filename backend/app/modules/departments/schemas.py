from pydantic import BaseModel, Field
from typing import Optional


class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

    model_config = {
        "from_attributes": True
    }


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)

    model_config = {
        "from_attributes": True
    }


class DepartmentResponse(DepartmentBase):
    id: int