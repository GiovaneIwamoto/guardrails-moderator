"""
SQLAlchemy ORM models for the moderation system database.
Defines tables for filter words and moderation logs.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from . import Base

class FilterWord(Base):
    """
    Model for a prohibited word in the moderation filter.
    """
    __tablename__ = "filter_words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True)

class ModerationLog(Base):
    """
    Model for logging moderation actions.
    """
    __tablename__ = "moderation_logs"
    id = Column(Integer, primary_key=True, index=True)
    original = Column(Text)
    moderated = Column(Text)
    method = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow) 