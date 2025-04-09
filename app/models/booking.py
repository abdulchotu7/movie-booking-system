"""
Booking model definition.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Booking(Base):
    """Booking model for storing ticket booking information."""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    showtime = Column(String)
    quantity = Column(Integer)
    total = Column(Integer)
    movie = relationship("Movie", backref="bookings")
