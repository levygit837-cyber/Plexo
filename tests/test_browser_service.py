import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.services.browser import BrowserManager


@pytest.mark.asyncio
async def test_start_profile_creates_context():
    manager = BrowserManager()

    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page = AsyncMock(return_value=mock_page)

    mock_browser = AsyncMock()
    mock_browser.new_context = AsyncMock(return_value=mock_context)

    with patch.object(manager, "_ensure_browser", new_callable=AsyncMock):
        manager._browser = mock_browser
        await manager.start_profile(
            profile_id="test-123",
            proxy_host="proxy.example.com",
            proxy_port=8080,
            proxy_username="user",
            proxy_password="pass",
            user_agent="Mozilla/5.0 Test",
            screen_width=1920,
            screen_height=1080,
            timezone="America/Sao_Paulo",
        )

    assert "test-123" in manager._contexts
    mock_browser.new_context.assert_called_once()


@pytest.mark.asyncio
async def test_stop_profile_closes_context():
    manager = BrowserManager()
    mock_context = AsyncMock()
    manager._contexts["test-123"] = mock_context

    await manager.stop_profile("test-123")

    mock_context.close.assert_called_once()
    assert "test-123" not in manager._contexts


@pytest.mark.asyncio
async def test_stop_nonexistent_profile():
    manager = BrowserManager()
    await manager.stop_profile("nonexistent")


def test_is_running():
    manager = BrowserManager()
    assert manager.is_running("test-123") is False
    manager._contexts["test-123"] = MagicMock()
    assert manager.is_running("test-123") is True
