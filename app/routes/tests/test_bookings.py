import pytest
from app.models.booking import Booking

def test_user_can_view_booking_page(client, test_movie, login_user):
    response = client.get("/book/1")
    assert response.status_code == 200
    assert "Test Movie" in response.text
    assert "Book Now" in response.text
    assert "Select Showtime" in response.text

def test_user_can_create_booking(client, test_movie, login_user):
    booking_data = {
        "movie_id": 1,
        "showtime": "14:00",
        "quantity": 2
    }
    response = client.post("/book", data=booking_data)
    assert response.status_code == 200

    response = client.get("/bookings")
    assert response.status_code == 200
    assert "Test Movie" in response.text
    assert "14:00" in response.text
    assert "$20" in response.text

def test_user_can_view_bookings(client, test_movie, login_user, db_session):
    booking = Booking(
        user="testuser",
        movie_id=1,
        showtime="2024-01-01 20:00",
        quantity=2,
        total=20
    )
    db_session.add(booking)
    db_session.commit()

    response = client.get("/bookings")
    assert response.status_code == 200
    assert "Test Movie" in response.text
    assert "20:00" in response.text
    assert "$20" in response.text

def test_user_can_cancel_booking(client, test_movie, login_user, db_session):
    booking = Booking(
        user="testuser",
        movie_id=1,
        showtime="2024-01-01 20:00",
        quantity=2,
        total=20
    )
    db_session.add(booking)
    db_session.commit()

    response = client.post("/cancel", data={"booking_id": 1})
    assert response.status_code == 200

    response = client.get("/bookings")
    assert "Test Movie" not in response.text
    assert "20:00" not in response.text

def test_booking_nonexistent_movie(client, login_user):
    response = client.get("/book/999")
    assert response.status_code == 404

