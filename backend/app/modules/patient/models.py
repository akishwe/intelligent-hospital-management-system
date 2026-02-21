from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base, TimestampMixin,SoftDeleteMixin
from sqlalchemy import Enum, Float, Boolean, ForeignKey, Text
from app.core.enums import Gender, BloodGroup,MaritalStatus

class Patient(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    mrn = Column(String(20), unique=True, index=True, nullable=False)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True, default="India")
    national_id = Column(String(50), nullable=True)
    insurance_provider = Column(String(100), nullable=True)
    insurance_number = Column(String(50), nullable=True)
    insurance_valid_till = Column(Date, nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(15), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    blood_group = Column(Enum(BloodGroup), nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    organ_donor = Column(Boolean, default=False)
    marital_status = Column(Enum(MaritalStatus), nullable=True)
    language = Column(String(50), nullable=True)
    religion = Column(String(50), nullable=True)
    occupation = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    photo = Column(String(255), nullable=True)
    preferred_pharmacy = Column(String(255), nullable=True)
    preferred_doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    