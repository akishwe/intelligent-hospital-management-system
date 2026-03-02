from app.core.database import Base
from sqlalchemy import Column, Integer, String
from app.core.database import TimestampMixin, SoftDeleteMixin

class Qualification(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "qualifications"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))