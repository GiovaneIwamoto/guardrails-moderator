"""
Service functions for managing moderation logs in the database.
Includes operations to add and retrieve logs.
"""
from sqlalchemy.orm import Session
from backend.db.models import ModerationLog
from datetime import datetime

# Add a new moderation log entry
def add_log(db: Session, original: str, moderated: str, method: str) -> None:
    """
    Adds a new moderation log entry to the database.
    """
    db.add(ModerationLog(original=original, moderated=moderated, method=method, timestamp=datetime.utcnow()))
    db.commit()

# Get recent moderation logs
def get_recent_logs(db: Session, limit: int = 10):
    """
    Returns the most recent moderation logs, limited by the specified number.
    """
    return db.query(ModerationLog).order_by(ModerationLog.timestamp.desc()).limit(limit).all()

# Get all moderation logs
def get_all_logs(db: Session):
    """
    Returns all moderation logs in the database.
    """
    return db.query(ModerationLog).order_by(ModerationLog.timestamp.desc()).all() 