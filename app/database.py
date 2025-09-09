"""Database session and engine configuration.

This module centralizes creation of the SQLAlchemy engine and session factory.
By default it uses a SQLite database file called `orion.db` in the project
root.  To use PostgreSQL or another backend, modify the `DATABASE_URL`
constant.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base

# Database connection string.  Use "postgresql+psycopg://user:pass@host/db"
# or similar to point at another RDBMS.
DATABASE_URL = "sqlite:///orion.db"

# Create engine and sessionmaker.  `future=True` and `echo=False` use
# SQLAlchemy's 2.0 style and suppress SQL logging unless needed.
engine = create_engine(DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Provide a transactional scope around a series of operations.

    This generator yields a new SQLAlchemy session and ensures that the
    connection is cleaned up after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
