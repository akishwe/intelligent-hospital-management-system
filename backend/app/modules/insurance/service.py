from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.insurance.models import Insurance
from app.modules.insurance.schemas import InsuranceCreate, InsuranceUpdate

class InsuranceService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Insurance]:
        return self.db.query(Insurance).offset(skip).limit(limit).all()

    def get_by_id(self, insurance_id: int) -> Optional[Insurance]:
        return self.db.query(Insurance).filter(Insurance.id == insurance_id).first()

    def create(self, insurance_data: InsuranceCreate) -> Insurance:
        insurance = Insurance(**insurance_data.model_dump())
        self.db.add(insurance)
        self.db.commit()
        self.db.refresh(insurance)
        return insurance

    def update(self, insurance_id: int, update_data: InsuranceUpdate) -> Optional[Insurance]:
        insurance = self.get_by_id(insurance_id)
        if not insurance:
            return None
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(insurance, field, value)
        self.db.commit()
        self.db.refresh(insurance)
        return insurance

    def delete(self, insurance_id: int) -> bool:
        insurance = self.get_by_id(insurance_id)
        if not insurance:
            return False
        self.db.delete(insurance)
        self.db.commit()
        return True

    def get_active_for_patient(self, patient_id: str) -> List[Insurance]:
        return self.db.query(Insurance).filter(Insurance.patient_id == patient_id, Insurance.active == True).all()