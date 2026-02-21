from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, Boolean,Enum, DateTime, Text, func, Date
from app.core.database import Base, TimestampMixin, SoftDeleteMixin
from app.core.enums import Gender
from app.core.enums import UserRole
class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    failed_attempts = Column(Integer, default=0)
    account_locked_until = Column(Date, nullable=True)
    department = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

class RevokedToken(TimestampMixin,Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, index=True, nullable=False)
    revoked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reason = Column(Text, nullable=True)

