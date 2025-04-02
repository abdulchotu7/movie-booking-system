from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, joinedload

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
    password = Column(String)  # Store hashed passwords in production!
 
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

# Booking Model with ForeignKey constraint and relationship to Movie
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))  # ForeignKey added here
    showtime = Column(String)
    quantity = Column(Integer)
    total = Column(Integer)
    movie = relationship("Movie", backref="bookings")

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")

# Seed movies into database
def seed_movies():
    db = SessionLocal()
    if db.query(Movie).count() == 0:
        movies = [
            Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8, format="IMAX", price=12),
            Movie(title="The Matrix", year=1999, director="The Wachowskis", rating=8.7, format="Standard", price=10),
            Movie(title="Avengers: Endgame", year=2019, director="Anthony and Joe Russo", rating=8.4, format="3D", price=15),
            Movie(title="The Godfather", year=1972, director="Francis Ford Coppola", rating=9.2, format="Standard", price=10),
            Movie(title="Pulp Fiction", year=1994, director="Quentin Tarantino", rating=8.9, format="Standard", price=10),
        ]
        db.add_all(movies)
        db.commit()
    db.close()

seed_movies()

# Helper function to enforce authentication
def require_login(request: Request):
    return request.session.get("user") is not None

# Home page: list movies (public page)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return templates.TemplateResponse("index.html", {"request": request, "movies": movies, "user": request.session.get("user")})

# Registration endpoints
@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return HTMLResponse("Username already exists. Please choose another.", status_code=400)
    db.add(User(username=username, password=password))
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

# Login endpoints
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if not user:
        return HTMLResponse("Invalid credentials", status_code=400)
    request.session["user"] = username
    return RedirectResponse(url="/", status_code=303)

# Logout endpoint
@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/login", status_code=303)

# Booking endpoints (require login)
@app.get("/book/{movie_id}", response_class=HTMLResponse)
async def book_movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return HTMLResponse("Movie not found", status_code=404)
    return templates.TemplateResponse("book.html", {"request": request, "movie": movie, "user": request.session.get("user")})

@app.post("/book")
async def create_booking(request: Request, movie_id: int = Form(...), showtime: str = Form(...), quantity: int = Form(...), db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return HTMLResponse("Movie not found", status_code=404)
    total_amount = movie.price * quantity
    booking = Booking(user=request.session["user"], movie_id=movie_id, showtime=showtime, quantity=quantity, total=total_amount)
    db.add(booking)
    db.commit()
    return RedirectResponse(url="/bookings", status_code=303)

@app.get("/bookings", response_class=HTMLResponse)
async def view_bookings(request: Request, db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)

    user_bookings = (
        db.query(Booking)
        .options(joinedload(Booking.movie))
        .filter(Booking.user == request.session["user"])
        .all()
    )

    bookings_with_movies = []
    for booking in user_bookings:
        bookings_with_movies.append({
            "id": booking.id,
            "movie": booking.movie.title if booking.movie else "Unknown",
            "showtime": booking.showtime,
            "price": booking.movie.price if booking.movie else 0,
            "quantity": booking.quantity,
            "total": booking.total
        })

    return templates.TemplateResponse("bookings.html", {"request": request, "bookings": bookings_with_movies, "user": request.session.get("user")})

@app.post("/cancel")
async def cancel_booking(request: Request, booking_id: int = Form(...), db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=303)
    db.query(Booking).filter(Booking.id == booking_id, Booking.user == request.session["user"]).delete()
    db.commit()
    return RedirectResponse(url="/bookings", status_code=303)
