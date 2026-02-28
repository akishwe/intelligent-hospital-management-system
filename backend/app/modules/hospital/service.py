from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List

from app.modules.hospital.models import Hospital
from app.modules.hospital.schemas import HospitalCreate, HospitalUpdate


class HospitalService:

    @staticmethod
    def create_hospital(db: Session, hospital_data: HospitalCreate) -> Hospital:
        hospital = Hospital(**hospital_data.model_dump())
        db.add(hospital)

        try:
            db.commit()
            db.refresh(hospital)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Hospital code '{hospital_data.code}' already exists."
            )

        return hospital

    @staticmethod
    def get_hospital(db: Session, hospital_id: int) -> Hospital:
        hospital = db.query(Hospital).filter(
            Hospital.id == hospital_id,
            Hospital.is_deleted == False
        ).first()

        if not hospital:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hospital not found"
            )

        return hospital

    @staticmethod
    def get_hospitals(db: Session, skip: int = 0, limit: int = 100) -> List[Hospital]:
        return (
            db.query(Hospital)
            .filter(Hospital.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_hospital(
        db: Session,
        hospital_id: int,
        hospital_data: HospitalUpdate
    ) -> Hospital:

        hospital = HospitalService.get_hospital(db, hospital_id)

        for key, value in hospital_data.model_dump(exclude_unset=True).items():
            setattr(hospital, key, value)

        try:
            db.commit()
            db.refresh(hospital)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hospital code already exists."
            )

        return hospital

    @staticmethod
    def delete_hospital(db: Session, hospital_id: int) -> dict:
        hospital = HospitalService.get_hospital(db, hospital_id)

        hospital.soft_delete()
        db.commit()

        return {"message": f"Hospital {hospital_id} deleted successfully"}