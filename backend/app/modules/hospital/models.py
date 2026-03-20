from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base, TimestampMixin, SoftDeleteMixin

user_hospital_association = Table(
    "user_hospital_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("hospital_id", Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), primary_key=True)
)

class Hospital(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    country = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    users = relationship(
        "User",
        secondary=user_hospital_association,
        back_populates="hospitals"
    )
    patients = relationship("Patient", back_populates="hospital")