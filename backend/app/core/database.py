from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings
from sqlalchemy import Column, DateTime, text,Boolean
from sqlalchemy.sql import func
from datetime import datetime,timezone

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TimestampMixin:
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False,nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None


Base = declarative_base()