
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Text, Date, Time, ForeignKey, func, UniqueConstraint
from app.core.enums import PersonType, ContactType
from sqlalchemy.types import Enum 
from app.core.database import TimestampMixin, SoftDeleteMixin
from sqlalchemy.orm import relationship


class Address(Base, TimestampMixin):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    line1 = Column(String(255), nullable=False)
    line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=False)
    timezone = Column(String(50), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint(
            "line1", "line2", "city", "state", "postal_code", "country",
            name="uq_full_address"
        ),
    )

class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    person_type = Column(Enum(PersonType), nullable=False)  
    person_id = Column(Integer, nullable=False)  
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    country_code = Column(String(5), nullable=True)
    email = Column(String(255), nullable=True)
    relation = Column(String(50), nullable=True)
    contact_type = Column(Enum(ContactType), nullable=False)
    preferred_contact = Column(Boolean, default=False)
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True)

    __table_args__ = (
        UniqueConstraint("person_type", "person_id", "contact_type", "phone", name="uq_person_contact"),
    )