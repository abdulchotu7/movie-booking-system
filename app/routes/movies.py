"""
Routes for viewing movies and the home page.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.movie import Movie
from app.config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Display the home page with a list of movies.
    """
    movies = db.query(Movie).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "movies": movies,
        "user": request.session.get("user"), 
        "is_admin": request.session.get("is_admin", False)
    })
