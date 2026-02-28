from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base, TimestampMixin

class Hospital(Base, TimestampMixin):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    country = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)