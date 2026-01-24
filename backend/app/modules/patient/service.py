from sqlalchemy import Session
from sqlalchemy.exc import IntegrityError
from app.modules.patient.models import Patient
from app.modules.patient.schemas import PatientCreate

class PatientService:

    def __init__(self, db: Session):
        self.db = db
    
    def create_patient(self, patient_data: PatientCreate) -> Patient:

        if not patient_data.phone_number.isdigit() or len(patient_data.phone_number) not in(10,12):
            raise ValueError("Invalid phone number format.")
        
        patient = Patient(**patient_data.model_dump())
        self.db.add(patient)
        try:
            self.db.commit()
            self.db.refresh(patient)
            return patient
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Phone number or email already exists.")
        
    def get_all_patients(self) -> list[Patient]:
        return self.db.query(Patient).all()
    
    def get_patient_by_id(self, patient_id: int) -> Patient | None:
        return self.db.query(Patient).filter(Patient.id == patient_id).first()