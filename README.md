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

- **Backend:** FastAPI, PostgreSQL, SQLAlchemy
- **Frontend:** Jinja2 Templates, Tailwind CSS
- **Testing:** pytest
- **Authentication:** Session-based authentication

## 📂 Project Structure

```text
📦 movie-booking-system
├── 📂 app/                    # Main application package
│   ├── 📂 models/             # Database models
│   │   ├── user.py            # User model
│   │   ├── movie.py           # Movie model
│   │   └── booking.py         # Booking model
│   ├── 📂 routes/             # API route handlers
│   │   ├── auth.py            # Authentication routes
│   │   ├── movies.py          # Movie routes
│   │   ├── bookings.py        # Booking routes
│   │   ├── admin.py           # Admin routes
│   │   └── 📂 tests/          # Test files for routes
│   ├── 📂 dependencies/       # Dependency functions
│   │   └── auth.py            # Authentication dependencies
│   ├── 📂 utils/              # Utility functions
│   │   └── seed.py            # Database seeding
│   ├── 📂 templates/          # HTML templates (Jinja2)
│   ├── 📜 main.py             # Application entry point
│   ├── 📜 config.py           # Configuration settings
│   └── 📜 database.py         # Database connection setup
├── 📜 .env                    # Environment variables (not in version control)
├── 📜 run.py                  # Script to run the application
├── 📜 requirements.txt        # Dependencies
├── 📜 pytest.ini              # pytest configuration
└── 📜 README.md               # Project documentation
```

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```sh
git clone https://github.com/abdulchotu7/movie-booking-system.git
cd movie-booking-system
```

### 2️⃣ Create virtual environment

```sh
python3 -m venv venv
source venv/bin/activate  
```

### 3️⃣ Install dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/movie_booking
SECRET_KEY=your-secret-key-32-chars-long
DEBUG=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=adminpass
```

### 5️⃣ Set up the database

After configuring your database connection in the `.env` file, run:

```sh
python3 run.py  # This will create the tables and seed initial data
```

### 6️⃣ Run the server

```sh
uvicorn app.main:app --reload
uvicorn app.main:app --reload
```

Access the app at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🔑 Admin Access

A default admin user is created on first run using the credentials specified in your `.env` file:

- **Username:** admin
- **Password:** adminpass

## 🧪 Testing

The application uses pytest for testing. To run the tests:

```sh
pytest
```

To run specific test files:

```sh
pytest app/routes/tests/test_movies.py
```

To run tests with verbose output:

```sh
pytest -v
```

### Test Database

Tests use an in-memory SQLite database by default. You can configure a separate test database in your `.env` file if needed.

## 🔧 Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Verify your PostgreSQL server is running
2. Check the `DATABASE_URL` in your `.env` file
3. Ensure the database exists and the user has appropriate permissions





💡 **Built with FastAPI for speed, security, and scalability!** 🚀
