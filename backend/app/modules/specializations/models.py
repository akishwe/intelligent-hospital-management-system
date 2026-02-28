from app.core.database import Base
from sqlalchemy import Column, Integer, String
from app.core.database import TimestampMixin, SoftDeleteMixin

class Specialization(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)