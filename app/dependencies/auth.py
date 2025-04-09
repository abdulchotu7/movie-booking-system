"""
Authentication and authorization dependencies.
"""
import logging
from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

def require_login(request: Request):
    """
    Dependency to check if a user is logged in.
    Raises HTTPException if not authenticated.
    """
    if not request.session.get("user"):
        logger.debug("Login required - no user in session")
        raise HTTPException(status_code=401, detail="Not authenticated")
    return True

def require_admin(request: Request, db: Session = Depends(get_db)):
    """
    Dependency to check if a user is an admin.
    Raises HTTPException if not an admin.
    """
    username = request.session.get("user")
    is_admin = request.session.get("is_admin", False)  
    
    if not username or not is_admin:
        logger.debug(f"Admin check failed for user {username}")
        raise HTTPException(status_code=403, detail="Admin privileges required")

    return db.query(User).filter(User.username == username, User.is_admin == True).first()
