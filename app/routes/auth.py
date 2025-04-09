"""
Authentication routes for user registration and login.
"""
import logging
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.user import User
from app.config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)
logger = logging.getLogger(__name__)

@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    """
    Display the registration form.
    """
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Process the registration form submission.
    """
    try:
        user = User(username=username, password=password)  
        db.add(user)
        db.commit()
        return RedirectResponse(url="/login", status_code=303)
    except IntegrityError:
        db.rollback()
        return HTMLResponse("Username already exists", status_code=400)

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    """
    Display the login form.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Process the login form submission.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or password != user.password:  
        return HTMLResponse("Invalid credentials", status_code=400)
    
    request.session["user"] = username
    request.session["is_admin"] = user.is_admin  
    logger.debug(f"User {username} logged in. Admin: {user.is_admin}")
    return RedirectResponse(url="/", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    """
    Log out the current user.
    """
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
