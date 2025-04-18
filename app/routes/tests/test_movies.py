import pytest
from app.models.movie import Movie

def test_view_movies_list(client, test_movie):
    response = client.get("/")
    assert response.status_code == 200
    assert "Test Movie" in response.text
    assert "Test Director" in response.text
    assert "2023" in response.text
    assert "$10" in response.text


def test_nonexistent_movie(client):
    response = client.get("/movies/999")
    assert response.status_code == 404
