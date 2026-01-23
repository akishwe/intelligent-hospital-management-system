from fastapi import APIRouter,HTTPException,status
from app.modules.patient.schemas import PatientCreate, PatientResponse
from app.modules.patient.service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate):
    try:
        return PatientService.create_patient(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    

