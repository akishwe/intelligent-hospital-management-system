from sqlalchemy.orm import Session
from app.modules.specialization.models import Specialization
from app.modules.specialization.schemas import SpecializationCreate, SpecializationUpdate
from app.core.exceptions import PatientException

class SpecializationService:

    def __init__(self, db: Session):
        self.db = db

    def create_specialization(self, specialization_data: SpecializationCreate, user_id: str = None):
        existing = self.db.query(Specialization).filter(
            Specialization.name == specialization_data.name
        ).first()
        if existing:
            raise PatientException(f"Specialization '{specialization_data.name}' already exists.")
        specialization = Specialization(**specialization_data.model_dump())
        self.db.add(specialization)
        self.db.commit()
        self.db.refresh(specialization)
        return specialization

    def get_specialization(self, specialization_id: int):
        specialization = self.db.query(Specialization).filter(
            Specialization.id == specialization_id
        ).first()
        if not specialization:
            raise PatientException("Specialization not found.")
        return specialization

    def get_specializations(self, skip: int = 0, limit: int = 100):
        return self.db.query(Specialization).offset(skip).limit(limit).all()

    def update_specialization(self, specialization_id: int, update_data: SpecializationUpdate, user_id: str = None):
        specialization = self.db.query(Specialization).filter(Specialization.id == specialization_id).first()
        if not specialization:
            raise PatientException("Specialization not found.")
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(specialization, field, value)
        self.db.commit()
        self.db.refresh(specialization)
        return specialization

    def delete_specialization(self, specialization_id: int, user_id: str = None):
        specialization = self.db.query(Specialization).filter(Specialization.id == specialization_id).first()
        if not specialization:
            raise PatientException("Specialization not found.")
        self.db.delete(specialization)
        self.db.commit()
        return {"detail": "Specialization deleted successfully."}