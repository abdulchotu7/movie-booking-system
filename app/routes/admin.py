
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.movie import Movie
from app.models.booking import Booking
from app.models.user import User
from app.dependencies.auth import require_admin
from app.config import TEMPLATES_DIR

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/movies", response_class=HTMLResponse)
async def admin_movies(
    request: Request,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
   
    movies = db.query(Movie).all()
    return templates.TemplateResponse("admin_movies.html", {
        "request": request,
        "movies": movies,
        "user": request.session.get("user"),
        "is_admin": True  
    })

@router.get("/movies/add", response_class=HTMLResponse)
async def add_movie_form(
    request: Request,
    admin_user: User = Depends(require_admin)
):
  
    return templates.TemplateResponse("admin_add_movie.html", {
        "request": request,
        "user": request.session.get("user"),
        "is_admin": True
    })

@router.post("/movies")
async def add_movie(
    request: Request,
    title: str = Form(...),
    year: int = Form(..., gt=1900, lt=2100),
    director: str = Form(...),
    rating: int = Form(..., ge=1, le=10),
    format: str = Form(...),
    price: int = Form(..., gt=0),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
   
    try:
        movie = Movie(
            title=title,
            year=year,
            director=director,
            rating=rating,
            format=format,
            price=price
        )
        db.add(movie)
        db.commit()
        return RedirectResponse(url="/admin/movies", status_code=200)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Movie already exists")

@router.get("/movies/{id}/edit", response_class=HTMLResponse)
async def edit_movie_form(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
   
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return templates.TemplateResponse("edit_movie.html", {
        "request": request,
        "movie": movie,
        "user": request.session.get("user"),
        "is_admin": True
    })

@router.post("/movies/{id}")
async def update_movie(
    request: Request,
    id: int,
    title: str = Form(...),
    year: int = Form(..., gt=1900, lt=2100),
    director: str = Form(...),
    rating: int = Form(..., ge=1, le=10),
    format: str = Form(...),
    price: int = Form(..., gt=0),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
   
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    try:
        movie.title = title
        movie.year = year
        movie.director = director
        movie.rating = rating
        movie.format = format
        movie.price = price
        db.commit()
        return RedirectResponse(url="/admin/movies", status_code=303)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Movie title already exists")

@router.post("/movies/{id}/delete")
async def delete_movie(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Delete a movie.
    """
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(movie)
    db.commit()
    return RedirectResponse(url="/admin/movies", status_code=303)

@router.get("/bookings", response_class=HTMLResponse)
async def admin_bookings(
    request: Request,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    
    bookings = (
        db.query(Booking)
        .options(joinedload(Booking.movie))
        .order_by(Booking.id)
        .all()
    )
    
    booking_data = []
    for booking in bookings:
        booking_data.append({
            "user": booking.user,
            "movie": booking.movie.title if booking.movie else "Unknown",
            "showtime": booking.showtime,
            "quantity": booking.quantity,
            "total": booking.total
        })
    
    return templates.TemplateResponse("admin_bookings.html", {
        "request": request,
        "bookings": booking_data,
        "user": request.session.get("user"),
        "is_admin": True
    })
