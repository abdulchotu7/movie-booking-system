"""
Import all route modules to make them available from the routes package.
"""
from app.routes.auth import router as auth_router
from app.routes.movies import router as movies_router
from app.routes.bookings import router as bookings_router
from app.routes.admin import router as admin_router