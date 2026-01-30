from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query
from app.core.deps import get_db
from app.modules.patient.schemas import PatientCreate, PatientResponse, PatientUpdate, PaginatedPatientResponse
from app.modules.patient.service import PatientService
from app.core.exceptions import InvalidPhoneNumber, DuplicatePatient, PatientNotFound
from app.core.deps import require_roles
from app.modules.auth.roles import UserRole
router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED,dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.DOCTOR, UserRole.RECEPTIONIST]))])
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    service = PatientService(db)
    try:
        patient = service.create_patient(payload)
        return patient
    except InvalidPhoneNumber as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicatePatient as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    


@router.get("/", response_model=PaginatedPatientResponse)
def get_all_patients(skip: int = Query(0, ge=0, description="Number of records to skip"), limit: int = Query(10, gt=0, le=100, description="Max number of records to return"),db: Session = Depends(get_db)):
    service = PatientService(db)
    patients, total = service.get_all_patients(skip=skip, limit=limit)
    return {"patients": patients, "total": total}


@router.get("/{patient_id}", response_model=PatientResponse,dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE]))])
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    patient = service.get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    
@router.put("/{patient_id}", response_model=PatientResponse,dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.DOCTOR]))])
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    service = PatientService(db)
    try:
        patient = service.update_patient(patient_id, payload)
        return patient
    except PatientNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidPhoneNumber as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicatePatient as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT,dependencies=[Depends(require_roles([UserRole.ADMIN]))])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    try:
        service.delete_patient(patient_id)
    except PatientNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    