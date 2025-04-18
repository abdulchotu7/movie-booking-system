import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.movie import Movie
from app.models.booking import Booking

# Create test database engine with a unique connection for each test session
@pytest.fixture(scope="function")
def engine():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency to use our test database
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session):
    user = User(username="testuser", password="testpass", is_admin=False)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_admin(db_session):
    admin = User(username="admin", password="adminpass", is_admin=True)
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def test_movie(db_session):
    movie = Movie(
        title="Test Movie",
        year=2023,
        director="Test Director",
        rating=8,
        format="Standard",
        price=10
    )
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return movie

@pytest.fixture
def login_user(client, test_user):
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200 or response.status_code == 303
    return response

@pytest.fixture
def login_admin(client, test_admin):
    response = client.post("/login", data={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200 or response.status_code == 303
    return response
