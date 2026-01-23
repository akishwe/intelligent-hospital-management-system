from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

Base = declarative_base()