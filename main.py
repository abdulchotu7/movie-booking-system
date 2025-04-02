from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, joinedload
from sqlalchemy.exc import IntegrityError
import logging

# Database setup
DATABASE_URL = "postgresql://postgres.wazswwkmwfdwaoxufkfx:capstone@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  
    is_admin = Column(Boolean, default=False)

# Movie Model
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    year = Column(Integer)
    director = Column(String)
    rating = Column(Integer)
    format = Column(String)
    price = Column(Integer)

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    showtime = Column(String)
    quantity = Column(Integer)
    total = Column(Integer)
    movie = relationship("Movie", backref="bookings")

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-32-chars-long")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Helper functions
def require_login(request: Request):
    if not request.session.get("user"):
        logger.debug("Login required - no user in session")
        raise HTTPException(status_code=401, detail="Not authenticated")
    return True

def require_admin(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("user")
    is_admin = request.session.get("is_admin", False)  
    
    if not username or not is_admin:
        logger.debug(f"Admin check failed for user {username}")
        raise HTTPException(status_code=403, detail="Admin privileges required")

    return db.query(User).filter(User.username == username, User.is_admin == True).first()



# Seed data
def seed_movies():
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

seed_movies()
create_admin()


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "movies": movies,
        "user": request.session.get("user"), 
        "is_admin": request.session.get("is_admin", False)
    })


# Authentication routes
@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = User(username=username, password=password)  
        db.add(user)
        db.commit()
        return RedirectResponse(url="/login", status_code=303)
    except IntegrityError:
        db.rollback()
        return HTMLResponse("Username already exists", status_code=400)

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or password != user.password:  
        return HTMLResponse("Invalid credentials", status_code=400)
    
    request.session["user"] = username
    request.session["is_admin"] = user.is_admin  
    logger.debug(f"User {username} logged in. Admin: {user.is_admin}")
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

# Booking routes
@app.get("/book/{movie_id}", response_class=HTMLResponse)
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

@app.post("/book")
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

@app.get("/bookings", response_class=HTMLResponse)
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

@app.post("/cancel")
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

# Admin routes (all protected with require_admin)
@app.get("/admin/movies", response_class=HTMLResponse)
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

@app.get("/admin/movies/add", response_class=HTMLResponse)
async def add_movie_form(
    request: Request,
    admin_user: User = Depends(require_admin)
):
    return templates.TemplateResponse("admin_add_movie.html", {
        "request": request,
        "user": request.session.get("user"),
        "is_admin": True
    })

@app.post("/admin/movies")
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
        return RedirectResponse(url="/admin/movies", status_code=303)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Movie already exists")

@app.get("/admin/movies/{id}/edit", response_class=HTMLResponse)
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

@app.post("/admin/movies/{id}")
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

@app.post("/admin/movies/{id}/delete")
async def delete_movie(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(movie)
    db.commit()
    return RedirectResponse(url="/admin/movies", status_code=303)

@app.get("/admin/bookings", response_class=HTMLResponse)
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