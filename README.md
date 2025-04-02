# 🎬 FastAPI Movie Ticket Booking System

## 🚀 Overview
This is a **FastAPI-based Movie Ticket Booking System** that allows users to:
- **View** movie listings.
- **Book** tickets for available movies.
- **Cancel** their bookings.
- **Admin users** can manage movies (add, update, delete) and view all bookings.

The application uses **JWT authentication**, **SQLAlchemy (PostgreSQL)** for database management, and **Tailwind CSS** for a modern UI.
## Live : 
https://movie-ebon-nu.vercel.app/

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
- **Deployment:** Vercel

## 📂 Project Structure
```
📦 movie-booking-app
├── 📂 templates               # HTML templates (Jinja2)
├── 📂 static                  # Static files (CSS, JS, images)
├── 📂 main.py                 # FastAPI application entry point
├── 📜 requirements.txt        # Dependencies
├── 📜 README.md               # Project documentation
```

## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
```sh
$ git clone https://github.com/yourusername/movie-booking-app.git
$ cd movie-booking-app
```

### 2️⃣ Install dependencies
```sh
$ pip install -r requirements.txt
```

### 3️⃣ Set up the database
Modify `DATABASE_URL` in `main.py` to match your PostgreSQL configuration.
Then, run:
```sh
$ python main.py  # This will create the tables
```

### 4️⃣ Run the server
```sh
$ uvicorn main:app --reload
```
Access the app at **http://127.0.0.1:8000**

## 🔑 Admin Access
A default admin user is created on first run:
- **Username:** `admin`
- **Password:** `adminpass`

## 🌐 Deployment on Vercel
### 1️⃣ Install Vercel CLI
```sh
$ npm install -g vercel
```

### 2️⃣ Deploy the app
```sh
$ vercel
```
Follow the on-screen instructions to deploy successfully.

## 🛠️ Future Improvements
- ✅ Payment gateway integration
- ✅ User seat selection feature
- ✅ Improved UI with React/Vue frontend


---

💡 **Built with FastAPI for speed, security, and scalability!** 🚀

