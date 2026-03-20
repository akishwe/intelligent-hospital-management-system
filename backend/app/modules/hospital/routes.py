from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.modules.hospital.schemas import HospitalCreate, HospitalUpdate, HospitalResponse
from app.modules.hospital.service import HospitalService
from app.core.database import get_db
from app.core.security import require_roles
from app.core.enums import UserRole

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

@router.post("/", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
def create_hospital(
    hospital_data: HospitalCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.SUPER_ADMIN]))
):
    return HospitalService.create_hospital(db, hospital_data)

@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
        UserRole.LAB_TECHNICIAN,
        UserRole.PHARMACIST,
        UserRole.RADIOLOGIST,
        UserRole.SURGEON,
        UserRole.PHYSIOTHERAPIST
    ]))
):
    return HospitalService.get_hospital(db, hospital_id)

@router.get("/", response_model=List[HospitalResponse])
def get_hospitals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    return HospitalService.get_hospitals(db, skip, limit)

@router.put("/{hospital_id}", response_model=HospitalResponse)
def update_hospital(
    hospital_id: int,
    hospital_data: HospitalUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    return HospitalService.update_hospital(db, hospital_id, hospital_data)

@router.delete("/{hospital_id}", status_code=status.HTTP_200_OK)
def delete_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.SUPER_ADMIN]))
):
    return HospitalService.delete_hospital(db, hospital_id)