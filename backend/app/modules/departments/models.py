from sqlalchemy import Column, Integer, String
from app.core.database import Base, TimestampMixin, SoftDeleteMixin

class Department(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)