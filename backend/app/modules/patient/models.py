from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base, TimestampMixin

class Patient(TimestampMixin, Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    phone_number = Column(String(15), nullable=False, unique=True)
    email = Column(String(255), nullable=True, unique=True)
    address = Column(String(500), nullable=True)
    