

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Enum, ForeignKey, Text, UniqueConstraint, DateTime
from app.core.database import Base, TimestampMixin, SoftDeleteMixin
from app.core.enums import Gender, BloodGroup, MaritalStatus, AdmissionStatus
from sqlalchemy.orm import relationship

class Patient(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    mrn = Column(String(20), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False, index=True)
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True)
    blood_group = Column(Enum(BloodGroup), nullable=True)
    marital_status = Column(Enum(MaritalStatus), nullable=True)
    organ_donor = Column(Boolean, default=False)
    preferred_language = Column(String(50), nullable=True)
    occupation = Column(String(100), nullable=True)
    hospital = relationship("Hospital", backref="patients")
    address = relationship("Address")
    allergies = relationship("Allergy", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    surgeries = relationship("Surgery", back_populates="patient", cascade="all, delete-orphan")
    admissions = relationship("Admission", back_populates="patient", cascade="all, delete-orphan")
    insurances = relationship("Insurance", back_populates="patient", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("hospital_id", "mrn", name="uq_hospital_mrn"),
        UniqueConstraint("hospital_id", "phone_number", name="uq_hospital_phone"),
        UniqueConstraint("hospital_id", "email", name="uq_hospital_email"),
    )



class Allergy(Base, TimestampMixin):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=True)
    reaction = Column(String(255), nullable=True)
    notes = Column(String(255), nullable=True)

    patient = relationship("Patient", back_populates="allergies")
    hospital = relationship("Hospital")

    __table_args__ = (
        UniqueConstraint("hospital_id", "patient_id", "name", name="uq_patient_allergy"),
    )


class Medication(Base, TimestampMixin):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=True)
    frequency = Column(String(50), nullable=True)
    route = Column(String(50), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    notes = Column(String(255), nullable=True)

    patient = relationship("Patient", back_populates="medications")
    hospital = relationship("Hospital")

    __table_args__ = (
        UniqueConstraint("hospital_id", "patient_id", "name", name="uq_patient_medication"),
    )


class Surgery(Base, TimestampMixin):
    __tablename__ = "surgeries"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    date = Column(Date, nullable=True)
    surgeon_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    anesthesia_type = Column(String(50), nullable=True)
    notes = Column(String(255), nullable=True)

    patient = relationship("Patient", back_populates="surgeries")
    hospital = relationship("Hospital")

    __table_args__ = (
        UniqueConstraint("hospital_id", "patient_id", "name", "date", name="uq_patient_surgery"),
    )


class Admission(TimestampMixin, Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    admission_date = Column(DateTime, nullable=False)
    discharge_date = Column(DateTime, nullable=True)
    ward = Column(String(50), nullable=True)
    room_number = Column(String(20), nullable=True)
    bed_number = Column(String(20), nullable=True)
    status = Column(Enum(AdmissionStatus), nullable=False)
    admitted_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reason_for_admission = Column(String(255), nullable=True)
    notes = Column(String(255), nullable=True)

    patient = relationship("Patient", back_populates="admissions")
    hospital = relationship("Hospital")
    admitted_user = relationship("User", foreign_keys=[admitted_by])

    __table_args__ = (
        UniqueConstraint("hospital_id", "patient_id", "admission_date", name="uq_patient_admission"),
    )
class Insurance(Base, TimestampMixin):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    provider_name = Column(String(100), nullable=False)
    policy_number = Column(String(50), nullable=False)
    coverage_type = Column(String(50), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    active = Column(Boolean, default=True)

    patient = relationship("Patient", back_populates="insurances")

    __table_args__ = (
        UniqueConstraint("patient_id", "provider_name", "policy_number", name="uq_patient_insurance"),
    )