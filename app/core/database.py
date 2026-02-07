from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Create the SQLAlchemy engine with environment-aware logging
# and automatic connection health checks
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models
class Base(DeclarativeBase):
    pass
