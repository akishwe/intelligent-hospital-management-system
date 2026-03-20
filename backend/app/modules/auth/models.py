from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Text, Date, Time, ForeignKey, func, UniqueConstraint
from app.core.database import Base, TimestampMixin, SoftDeleteMixin
from app.core.enums import Gender, UserRole
from datetime import datetime
from sqlalchemy.orm import relationship,backref

class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    staff_id = Column(String(50), nullable=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=True)
    date_of_birth = Column(DateTime(timezone=True), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="SET NULL"), nullable=True, index=True)
    created_by = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    deleted_by = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)

    role = Column(Enum(UserRole), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)  
    qualification_id = Column(Integer, ForeignKey("qualifications.id", ondelete="SET NULL"), nullable=True) 
    specialization_id = Column(Integer, ForeignKey("specializations.id", ondelete="SET NULL"), nullable=True)  
    experience_years = Column(Integer, nullable=True)
    shift_start = Column(Time(timezone=True), nullable=True)
    shift_end = Column(Time(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    two_factor_enabled = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    national_id = Column(String(50), nullable=True, index=True)
    profile_photo = Column(String(255), nullable=True)
    hospital = relationship(
        "Hospital",
        backref=backref(
            "patients",
            lazy='dynamic',
            primaryjoin="and_(Patient.hospital_id==Hospital.id, Patient.is_deleted==False)"
        )
    )
    department = relationship("Department")
    qualification = relationship("Qualification")
    specialization = relationship("Specialization")
    __table_args__ = (
        UniqueConstraint("hospital_id", "email", name="uq_user_hospital_email"),
        UniqueConstraint("hospital_id", "phone_number", name="uq_user_hospital_phone"),
        UniqueConstraint("hospital_id", "staff_id", name="uq_user_hospital_staff"),
        UniqueConstraint("hospital_id", "national_id", name="uq_user_hospital_national_id"),
    )


class RevokedToken(TimestampMixin, Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, index=True, nullable=False)
    revoked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reason = Column(Text, nullable=True)


class RefreshToken(TimestampMixin, Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_jti = Column(String(255), nullable=True, index=True)
    token = Column(String(500), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User")