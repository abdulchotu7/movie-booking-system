
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.movie import Movie
from app.models.booking import Booking
from app.dependencies.auth import require_login
from app.config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/book/{movie_id}", response_class=HTMLResponse)
async def book_movie(
    request: Request,
    movie_id: int,
    db: Session = Depends(get_db)
):
   
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return templates.TemplateResponse("book.html", {
        "request": request,
        "movie": movie,
        "user": request.session.get("user"),
        "is_admin": request.session.get("is_admin", False)
    })

@router.post("/book")
async def create_booking(
    request: Request,
    movie_id: int = Form(...),
    showtime: str = Form(...),
    quantity: int = Form(..., gt=0),
    db: Session = Depends(get_db)
):
    
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    total_amount = movie.price * quantity
    booking = Booking(
        user=request.session["user"],
        movie_id=movie_id,
        showtime=showtime,
        quantity=quantity,
        total=total_amount
    )
    
    db.add(booking)
    db.commit()
    return RedirectResponse(url="/bookings", status_code=303)

@router.get("/bookings", response_class=HTMLResponse)
async def view_bookings(request: Request, db: Session = Depends(get_db)):
  
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    
    bookings = (
        db.query(Booking)
        .options(joinedload(Booking.movie))
        .filter(Booking.user == request.session["user"])
        .all()
    )
    
    return templates.TemplateResponse("bookings.html", {
        "request": request,
        "bookings": bookings,
        "user": request.session.get("user"),
        "is_admin": request.session.get("is_admin", False)
    })

@router.post("/cancel")
async def cancel_booking(
    request: Request,
    booking_id: int = Form(...),
    db: Session = Depends(get_db)
):
   
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    
    db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user == request.session["user"]
    ).delete()
    db.commit()
    return RedirectResponse(url="/bookings", status_code=303)
