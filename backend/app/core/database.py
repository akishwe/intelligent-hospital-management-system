from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings
from sqlalchemy import Column, DateTime, text,Boolean,String,ForeignKey
from sqlalchemy.sql import func
from datetime import datetime,timezone

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TimestampMixin:
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    created_by = Column(String(255), ForeignKey('users.id'), nullable=True)
    updated_by = Column(String(255), ForeignKey('users.id'), nullable=True)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False,nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String(255), ForeignKey('users.id'), nullable=True)

    def soft_delete(self, user_id: str = None):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        if user_id:
            self.deleted_by = user_id


    def restore(self):
        self.is_deleted = False
        self.deleted_at = None


Base = declarative_base()