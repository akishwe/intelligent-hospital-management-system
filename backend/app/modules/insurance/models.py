from sqlalchemy import Column, Integer, String, Boolean, Date, Float, ForeignKey, UniqueConstraint
from app.core.database import Base, TimestampMixin, SoftDeleteMixin
from sqlalchemy.orm import relationship

class Insurance(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    provider_name = Column(String(100), nullable=False)
    provider_code = Column(String(50), nullable=True)
    policy_number = Column(String(50), nullable=False)
    coverage_type = Column(String(50), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    active = Column(Boolean, default=True)
    coverage_limit = Column(Float, nullable=True)
    currency = Column(String(3), nullable=True)
    external_reference = Column(String(100), nullable=True)

    patient = relationship("Patient", back_populates="insurances")

    __table_args__ = (
        UniqueConstraint(
            "patient_id", "provider_name", "policy_number", name="uq_patient_insurance"
        ),
    )