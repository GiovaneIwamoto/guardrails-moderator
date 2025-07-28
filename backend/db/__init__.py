"""
Database initialization and session management for the moderation backend.
Uses SQLAlchemy ORM and SQLite by default.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL (default: SQLite local file)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./moderator.db")
# SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for models
Base = declarative_base() 