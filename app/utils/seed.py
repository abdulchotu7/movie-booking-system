"""
Utility functions for seeding initial data.
"""
import logging
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.movie import Movie

logger = logging.getLogger(__name__)

def seed_movies():
    """
    Seed the database with initial movie data if none exists.
    """
    db = SessionLocal()
    try:
        if db.query(Movie).count() == 0:
            movies = [
                Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8, format="IMAX", price=12),
                Movie(title="The Matrix", year=1999, director="The Wachowskis", rating=8, format="Standard", price=10),
                Movie(title="Avengers: Endgame", year=2019, director="Anthony and Joe Russo", rating=8, format="3D", price=15),
            ]
            db.add_all(movies)
            db.commit()
    finally:
        db.close()

def create_admin():
    """
    Create an admin user if none exists.
    """
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password="adminpass",  
                is_admin=True
            )
            db.add(admin)
            db.commit()
            logger.debug("Admin user created")
    finally:
        db.close()

def initialize_data():
    """
    Initialize all seed data.
    """
    seed_movies()
    create_admin()
