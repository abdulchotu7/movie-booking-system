# 🎬 FastAPI Movie Ticket Booking System

## 🚀 Overview
This is a **FastAPI-based Movie Ticket Booking System** that allows users to:
- **View** movie listings.
- **Book** tickets for available movies.
- **Cancel** their bookings.
- **Admin users** can manage movies (add, update, delete) and view all bookings.

The application uses **Sessions**, **PostgreSQL** for database management, and **Tailwind CSS** for a modern UI.


## 🛠️ Features
### ✅ User Features
- User **registration & login** (session-based authentication)
- Browse movies and **book tickets** (multiple bookings per movie allowed)
- **Cancel bookings**
- View **personal booking history**

### 🛡️ Admin Features
- **Add, update, delete** movies
- View **all user bookings**
- Protected admin routes using **role-based authentication**

## 🏗️ Tech Stack
- **Backend:** FastAPI, PostgreSQL
- **Frontend:** Jinja2 Templates, Tailwind CSS

## 📂 Project Structure
```
📦 movie-booking-app
├── 📂 app/                    # Main application package
│   ├── 📂 models/             # Database models
│   │   ├── user.py
│   │   ├── movie.py
│   │   └── booking.py
│   ├── 📂 routes/             # API route handlers
│   │   ├── auth.py
│   │   ├── movies.py
│   │   ├── bookings.py
│   │   └── admin.py
│   ├── 📂 dependencies/       # Dependency functions
│   │   └── auth.py
│   ├── 📂 utils/              # Utility functions
│   │   └── seed.py
│   ├── 📂 templates/          # HTML templates (Jinja2)
│   ├── 📜 main.py             # Application entry point
│   ├── 📜 config.py           # Configuration settings
│   └── 📜 database.py         # Database connection setup
├── 📜 .env                    # Environment variables (not in version control)
├── 📜 run.py                  # Script to run the application
├── 📜 requirements.txt        # Dependencies
└── 📜 README.md               # Project documentation
```

## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
```sh
git clone https://github.com/abdulchotu7/movie-booking-system.git
cd movie-booking-system
```

### Create virtual environment
```sh
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
```

### 2️⃣ Install dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables

Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=postgresql://username:password@localhost:5432/movie_booking
SECRET_KEY=your-secret-key-32-chars-long
DEBUG=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=adminpass
```


### 4️⃣ Set up the database

After configuring your database connection in the `.env` file, run:

```sh
python3 run.py  # This will create the tables
```

### 4️⃣ Run the server
```sh
uvicorn app.main:app --reload
```
Access the app at **http://127.0.0.1:8000**

## 🔑 Admin Access
A default admin user is created on first run using the credentials specified in your `.env` file:
- **Username:** admin
- **Password:** adminpass


💡 **Built with FastAPI for speed, security, and scalability!** 🚀
