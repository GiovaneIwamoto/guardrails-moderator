"""
Service functions for managing prohibited words (word filter) in the database.
Includes operations to get, add, and delete filter words.
"""
from sqlalchemy.orm import Session
from backend.db.models import FilterWord

# Get all prohibited words from the database
def get_prohibited_words(db: Session) -> set:
    """
    Returns a set of all prohibited words in lowercase.
    """
    return set(row.word.lower() for row in db.query(FilterWord).all())

# Add a new prohibited word
def add_filter_word(db: Session, word: str) -> None:
    """
    Adds a new word to the filter list if it does not already exist.
    """
    word = word.strip().lower()
    if not db.query(FilterWord).filter_by(word=word).first():
        db.add(FilterWord(word=word))
        db.commit()

# Delete a prohibited word by ID
def delete_filter_word(db: Session, filter_id: int) -> None:
    """
    Deletes a word from the filter list by its ID.
    """
    filter_word = db.query(FilterWord).filter_by(id=filter_id).first()
    if filter_word:
        db.delete(filter_word)
        db.commit() 