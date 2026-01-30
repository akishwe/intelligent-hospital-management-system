from sqlalchemy import Column, Integer, String, Boolean,Enum
from app.core.database import Base, TimestampMixin
from app.modules.auth.roles import UserRole

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender  = Column(String(10), nullable=True)
    date_of_birth = Column(String(10), nullable=True)
    address = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False) 

