from sqlalchemy.orm import Session
from typing import Tuple, List
from sqlalchemy.exc import IntegrityError
from app.modules.patient.models import Patient
from app.modules.patient.schemas import PatientCreate, PatientUpdate
from app.core.exceptions import PatientNotFound, InvalidPhoneNumber, DuplicatePatient

class PatientService:

    def __init__(self, db: Session):
        self.db = db

    def get_patient_by_id(self, patient_id: int) -> Patient:
        patient = (
            self.db.query(Patient)
            .filter(Patient.id == patient_id,Patient.is_deleted == False)
            .first()
        )
        if not patient:
            raise PatientNotFound()
        return patient

    def create_patient(self, patient_data: PatientCreate) -> Patient:
        if not patient_data.phone_number.isdigit() or len(patient_data.phone_number) not in (10, 12):
            raise InvalidPhoneNumber()

        patient = Patient(**patient_data.model_dump())
        self.db.add(patient)

        try:
            self.db.commit()
            self.db.refresh(patient)
            return patient
        except IntegrityError:
            self.db.rollback()
            raise DuplicatePatient()

    def update_patient(self, patient_id: int, data: PatientUpdate) -> Patient:
        patient = self.get_patient_by_id(patient_id)

        if data.phone_number:
            if not data.phone_number.isdigit() or len(data.phone_number) not in (10, 12):
                raise InvalidPhoneNumber()

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)

        try:
            self.db.commit()
            self.db.refresh(patient)
            return patient
        except IntegrityError:
            self.db.rollback()
            raise DuplicatePatient()

    def delete_patient(self, patient_id: int) -> None:
        patient = self.get_patient_by_id(patient_id)
        patient.soft_delete(patient)
        self.db.commit()

    def get_all_patients(self, skip: int = 0, limit: int = 10) -> Tuple[List[Patient], int]:
        total = self.db.query(Patient).count()
        patients = self.db.query(Patient).offset(skip).limit(limit).all()
        return patients, total