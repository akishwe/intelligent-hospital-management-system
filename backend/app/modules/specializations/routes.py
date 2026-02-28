from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.modules.specialization.schemas import SpecializationCreate, SpecializationUpdate, SpecializationResponse
from app.modules.specialization.service import SpecializationService
from app.core.database import get_db
from app.core.deps import require_roles
from app.core.enums import UserRole

router = APIRouter(prefix="/specializations", tags=["Specializations"])

@router.get("/", response_model=List[SpecializationResponse])
def list_specializations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE
    ]))
):
    service = SpecializationService(db)
    return service.get_specializations(skip, limit)

@router.get("/{specialization_id}", response_model=SpecializationResponse)
def get_specialization(
    specialization_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE
    ]))
):
    service = SpecializationService(db)
    specialization = service.get_specialization(specialization_id)
    if not specialization:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return specialization

@router.post("/", response_model=SpecializationResponse, status_code=status.HTTP_201_CREATED)
def create_specialization(
    specialization: SpecializationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    service = SpecializationService(db)
    return service.create_specialization(specialization, user_id=current_user["id"])

@router.patch("/{specialization_id}", response_model=SpecializationResponse)
def update_specialization(
    specialization_id: int,
    update_data: SpecializationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    service = SpecializationService(db)
    specialization = service.update_specialization(specialization_id, update_data, user_id=current_user["id"])
    if not specialization:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return specialization

@router.delete("/{specialization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_specialization(
    specialization_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN]))
):
    service = SpecializationService(db)
    service.delete_specialization(specialization_id, user_id=current_user["id"])
    return None