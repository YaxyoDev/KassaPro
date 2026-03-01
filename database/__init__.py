from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.models import Base

# Database engine yaratish
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Database jadvallarini yaratish"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Session olish"""
    return SessionLocal()


def close_session(session):
    """Session yopish"""
    if session:
        session.close()