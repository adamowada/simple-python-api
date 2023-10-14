from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration
DATABASE_URL = "sqlite:///./merch_store.db"  # Using SQLite for simplicity

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)


def init_db():
    """Call this function to create all tables in the database."""
    from .models import Base
    Base.metadata.create_all(bind=engine)
