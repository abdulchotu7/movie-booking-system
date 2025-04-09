"""
Movie model definition.
"""
from sqlalchemy import Column, Integer, String

from app.database import Base

class Movie(Base):
    """Movie model for storing movie information."""
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    year = Column(Integer)
    director = Column(String)
    rating = Column(Integer)
    format = Column(String)
    price = Column(Integer)
