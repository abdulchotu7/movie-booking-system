import pytest
from app.models.booking import Booking

def test_admin_can_view_movies(client, test_movie, login_admin):
    response = client.get("/admin/movies")
    assert response.status_code == 200
    assert "Test Movie" in response.text

def test_admin_can_add_movie(client, test_movie, login_admin):
    movie_data = {
        "title": "New Test Movie",
        "year": 2024,
        "director": "New Director",
        "rating": 9,
        "format": "IMAX",
        "price": 15
    }
    response = client.post("/admin/movies", data=movie_data)
    assert response.status_code == 200

    response = client.get("/admin/movies")
    assert "New Test Movie" in response.text

def test_admin_can_delete_movie(client, test_movie, login_admin):
    response = client.post("/admin/movies/1/delete")
    assert response.status_code == 200

    response = client.get("/admin/movies")
    assert "Test Movie" not in response.text

def test_admin_can_view_bookings(client, test_movie, login_admin, db_session):
    booking = Booking(
        user="testuser",
        movie_id=1,
        showtime="2024-01-01 20:00",
        quantity=2,
        total=20
    )
    db_session.add(booking)
    db_session.commit()

    response = client.get("/admin/bookings")
    assert response.status_code == 200
    assert "testuser" in response.text
    assert "Test Movie" in response.text
