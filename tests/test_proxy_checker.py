import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.services.proxy_checker import check_proxy, ProxyCheckResult


@pytest.mark.asyncio
async def test_check_proxy_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "query": "1.2.3.4",
        "city": "Sao Paulo",
        "country": "Brazil",
        "timezone": "America/Sao_Paulo",
    }

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("backend.services.proxy_checker.httpx.AsyncClient", return_value=mock_client):
        result = await check_proxy("proxy.example.com", 8080, "user", "pass")

    assert isinstance(result, ProxyCheckResult)
    assert result.valid is True
    assert result.ip == "1.2.3.4"
    assert result.city == "Sao Paulo"
    assert result.country == "Brazil"
    assert result.timezone == "America/Sao_Paulo"


@pytest.mark.asyncio
async def test_check_proxy_failure():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=Exception("Connection failed"))

    with patch("backend.services.proxy_checker.httpx.AsyncClient", return_value=mock_client):
        result = await check_proxy("bad.proxy.com", 9999)

    assert result.valid is False
    assert result.error == "Connection failed"
