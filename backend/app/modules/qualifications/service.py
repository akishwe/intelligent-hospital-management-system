from sqlalchemy.orm import Session
from app.modules.qualifications.models import Qualification
from app.modules.qualifications.schemas import QualificationCreate, QualificationUpdate
from app.core.exceptions import PatientException
from datetime import datetime

class QualificationService:

    def __init__(self, db: Session):
        self.db = db

    def create_qualification(self, data: QualificationCreate, user_id: str = None):
        existing = self.db.query(Qualification).filter(Qualification.name == data.name).first()
        if existing:
            raise PatientException(f"Qualification '{data.name}' already exists.")
        qualification = Qualification(**data.model_dump())
        self.db.add(qualification)
        self.db.commit()
        self.db.refresh(qualification)
        return qualification

    def get_qualification(self, qualification_id: int):
        qualification = self.db.query(Qualification).filter(Qualification.id == qualification_id).first()
        if not qualification:
            raise PatientException("Qualification not found.")
        return qualification

    def get_qualifications(self, skip: int = 0, limit: int = 100):
        return self.db.query(Qualification).offset(skip).limit(limit).all()

    def update_qualification(self, qualification_id: int, update_data: QualificationUpdate, user_id: str = None):
        qualification = self.db.query(Qualification).filter(Qualification.id == qualification_id).first()
        if not qualification:
            raise PatientException("Qualification not found.")
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(qualification, field, value)
        self.db.commit()
        self.db.refresh(qualification)
        return qualification

    def delete_qualification(self, qualification_id: int, user_id: str = None):
        qualification = self.db.query(Qualification).filter(Qualification.id == qualification_id).first()
        if not qualification:
            raise PatientException("Qualification not found.")
        qualification.is_deleted = True
        qualification.deleted_at = datetime.now()
        qualification.deleted_by = user_id
        self.db.commit()
        return {"detail": "Qualification soft-deleted successfully."}