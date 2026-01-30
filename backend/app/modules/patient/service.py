import uuid
from sqlalchemy.orm import Session
from typing import Tuple, List
from sqlalchemy.exc import IntegrityError
from app.modules.patient.models import Patient
from app.modules.patient.schemas import PatientCreate, PatientUpdate
from app.core.exceptions import PatientNotFound, InvalidPhoneNumber, DuplicatePatient
from app.core.logging import get_logger

logger = get_logger("patients")

class PatientService:

    def __init__(self, db: Session):
        self.db = db

    def get_patient_by_id(self, patient_id: int) -> Patient:
        patient = (
            self.db.query(Patient)
            .filter(Patient.id == patient_id, Patient.is_deleted == False)
            .first()
        )
        if not patient:
            logger.warning(f"Patient not found | patient_id={patient_id}")
            raise PatientNotFound()
        logger.debug(f"Fetched patient | patient_id={patient.id} | MRN={patient.mrn}")
        return patient

    def create_patient(self, patient_data: PatientCreate) -> Patient:
        patient = Patient(**patient_data.model_dump())
        patient.mrn = "MRN-" + uuid.uuid4().hex[:8].upper()
        self.db.add(patient)

        try:
            self.db.commit()
            self.db.refresh(patient)
            logger.info(f"Patient created | id={patient.id} | MRN={patient.mrn}")
            return patient
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Failed to create patient | error={str(e)}")
            raise DuplicatePatient()

    def update_patient(self, patient_id: int, data: PatientUpdate) -> Patient:
        patient = self.get_patient_by_id(patient_id)

        if data.phone_number:
            if not data.phone_number.isdigit() or len(data.phone_number) not in (10, 12):
                logger.warning(f"Invalid phone number attempt | patient_id={patient_id} | phone={data.phone_number}")
                raise InvalidPhoneNumber()

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)

        try:
            self.db.commit()
            self.db.refresh(patient)
            logger.info(f"Patient updated | id={patient.id} | MRN={patient.mrn}")
            return patient
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Failed to update patient | patient_id={patient_id} | error={str(e)}")
            raise DuplicatePatient()

    def delete_patient(self, patient_id: int) -> None:
        patient = self.get_patient_by_id(patient_id)
        patient.soft_delete()
        self.db.commit()
        logger.info(f"Patient soft deleted | id={patient.id} | MRN={patient.mrn}")

    def get_all_patients(self, skip: int = 0, limit: int = 10) -> Tuple[List[Patient], int]:
        total = self.db.query(Patient).count()
        patients = self.db.query(Patient).offset(skip).limit(limit).all()
        logger.debug(f"Fetched all patients | count={len(patients)} | total={total}")
        return patients, total