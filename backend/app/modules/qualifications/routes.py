from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.modules.qualifications.schemas import QualificationCreate, QualificationUpdate, QualificationResponse
from app.modules.qualifications.service import QualificationService
from app.core.database import get_db
from app.core.deps import require_roles
from app.core.enums import UserRole

router = APIRouter(prefix="/qualifications", tags=["Qualifications"])

@router.get("/", response_model=List[QualificationResponse])
def list_qualifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
        UserRole.PHARMACIST,
        UserRole.ACCOUNTANT,
        UserRole.BILLING_OFFICER,
        UserRole.RADIOLOGIST,
        UserRole.SURGEON,
        UserRole.PHYSIOTHERAPIST
    ]))
):
    service = QualificationService(db)
    return service.get_qualifications(skip, limit)

@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(
    qualification_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
        UserRole.PHARMACIST,
        UserRole.ACCOUNTANT,
        UserRole.BILLING_OFFICER,
        UserRole.RADIOLOGIST,
        UserRole.SURGEON,
        UserRole.PHYSIOTHERAPIST
    ]))
):
    service = QualificationService(db)
    qualification = service.get_qualification(qualification_id)
    if not qualification:
        raise HTTPException(status_code=404, detail="Qualification not found")
    return qualification

@router.post("/", response_model=QualificationResponse, status_code=status.HTTP_201_CREATED)
def create_qualification(
    qualification: QualificationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN
    ]))
):
    service = QualificationService(db)
    return service.create_qualification(qualification, user_id=current_user["id"])

@router.patch("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(
    qualification_id: int,
    update_data: QualificationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN
    ]))
):
    service = QualificationService(db)
    qualification = service.update_qualification(qualification_id, update_data, user_id=current_user["id"])
    if not qualification:
        raise HTTPException(status_code=404, detail="Qualification not found")
    return qualification

@router.delete("/{qualification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qualification(
    qualification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN]))
):
    service = QualificationService(db)
    service.delete_qualification(qualification_id, user_id=current_user["id"])
    return None