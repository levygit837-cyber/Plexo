import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.proxy_checker import ProxyCheckResult


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client


def test_parse_proxy_webshare(client: TestClient):
    response = client.post(
        "/api/proxy/parse",
        json={"raw": "proxy.example.com:8080:user:pass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["host"] == "proxy.example.com"
    assert data["port"] == 8080
    assert data["username"] == "user"
    assert data["password"] == "pass"


def test_parse_proxy_invalid(client: TestClient):
    response = client.post(
        "/api/proxy/parse",
        json={"raw": "invalid"},
    )
    assert response.status_code == 400


def test_validate_proxy(client: TestClient):
    mock_result = ProxyCheckResult(
        valid=True,
        ip="1.2.3.4",
        city="Sao Paulo",
        country="Brazil",
        timezone="America/Sao_Paulo",
    )

    with patch(
        "backend.routers.proxy.check_proxy",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = client.post(
            "/api/proxy/validate",
            json={
                "host": "proxy.example.com",
                "port": 8080,
                "username": "user",
                "password": "pass",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["ip"] == "1.2.3.4"
    assert data["timezone"] == "America/Sao_Paulo"
