import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app
from backend.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_profile(client: TestClient):
    response = client.post(
        "/api/profiles",
        json={
            "name": "Test Profile",
            "user_agent": "Mozilla/5.0 Chrome/120",
            "screen_width": 1920,
            "screen_height": 1080,
            "proxy_host": "proxy.example.com",
            "proxy_port": 8080,
            "proxy_username": "user",
            "proxy_password": "pass",
            "timezone": "America/Sao_Paulo",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Profile"
    assert data["status"] == "stopped"
    assert "id" in data


def test_list_profiles(client: TestClient):
    client.post("/api/profiles", json={"name": "Profile 1"})
    client.post("/api/profiles", json={"name": "Profile 2"})

    response = client.get("/api/profiles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_profile(client: TestClient):
    create_resp = client.post("/api/profiles", json={"name": "My Profile"})
    profile_id = create_resp.json()["id"]

    response = client.get(f"/api/profiles/{profile_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "My Profile"


def test_get_profile_not_found(client: TestClient):
    response = client.get("/api/profiles/nonexistent-id")
    assert response.status_code == 404


def test_update_profile(client: TestClient):
    create_resp = client.post("/api/profiles", json={"name": "Old Name"})
    profile_id = create_resp.json()["id"]

    response = client.put(
        f"/api/profiles/{profile_id}",
        json={"name": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_profile(client: TestClient):
    create_resp = client.post("/api/profiles", json={"name": "To Delete"})
    profile_id = create_resp.json()["id"]

    response = client.delete(f"/api/profiles/{profile_id}")
    assert response.status_code == 200

    get_resp = client.get(f"/api/profiles/{profile_id}")
    assert get_resp.status_code == 404


def test_start_profile(client: TestClient):
    create_resp = client.post(
        "/api/profiles",
        json={
            "name": "Browser Profile",
            "proxy_host": "proxy.example.com",
            "proxy_port": 8080,
        },
    )
    profile_id = create_resp.json()["id"]

    with patch(
        "backend.routers.profiles.browser_manager.start_profile",
        new_callable=AsyncMock,
    ) as mock_start:
        response = client.post(f"/api/profiles/{profile_id}/start")

    assert response.status_code == 200
    assert response.json()["status"] == "running"
    mock_start.assert_called_once()


def test_stop_profile(client: TestClient):
    create_resp = client.post("/api/profiles", json={"name": "To Stop"})
    profile_id = create_resp.json()["id"]

    with patch(
        "backend.routers.profiles.browser_manager.start_profile",
        new_callable=AsyncMock,
    ):
        client.post(f"/api/profiles/{profile_id}/start")

    with patch(
        "backend.routers.profiles.browser_manager.stop_profile",
        new_callable=AsyncMock,
    ) as mock_stop:
        response = client.post(f"/api/profiles/{profile_id}/stop")

    assert response.status_code == 200
    assert response.json()["status"] == "stopped"
    mock_stop.assert_called_once()
