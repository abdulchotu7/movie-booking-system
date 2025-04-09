"""
Main application entry point.
"""
import logging
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import SECRET_KEY, DEBUG
from app.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.movies import router as movies_router
from app.routes.bookings import router as bookings_router
from app.routes.admin import router as admin_router
from app.utils.seed import initialize_data

# Configure logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(
    title="Movie Booking System",
    description="A web application for booking movie tickets",
    version="1.0.0"
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Include routers
app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(bookings_router)
app.include_router(admin_router)

# Initialize seed data
@app.on_event("startup")
async def startup_event():
    """
    Initialize seed data on application startup.
    """
    initialize_data()
    logger.info("Application started and seed data initialized")
