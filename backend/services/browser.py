import os
from typing import Optional

from playwright.async_api import async_playwright, Browser, BrowserContext

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "browser_data")
os.makedirs(DATA_DIR, exist_ok=True)


class BrowserManager:
    """Manages isolated Chromium browser contexts per profile."""

    def __init__(self):
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._contexts: dict[str, BrowserContext] = {}

    async def _ensure_browser(self):
        """Launch Playwright and Chromium if not already running."""
        if self._browser is None:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )

    async def start_profile(
        self,
        profile_id: str,
        proxy_host: Optional[str] = None,
        proxy_port: Optional[int] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        user_agent: Optional[str] = None,
        screen_width: int = 1920,
        screen_height: int = 1080,
        timezone: Optional[str] = None,
    ) -> None:
        """Start an isolated browser context for a profile."""
        if profile_id in self._contexts:
            return

        await self._ensure_browser()

        context_options = {
            "viewport": {"width": screen_width, "height": screen_height},
            "no_viewport": False,
        }

        if user_agent:
            context_options["user_agent"] = user_agent

        if timezone:
            context_options["timezone_id"] = timezone

        if proxy_host and proxy_port:
            proxy_config = {
                "server": f"http://{proxy_host}:{proxy_port}",
            }
            if proxy_username and proxy_password:
                proxy_config["username"] = proxy_username
                proxy_config["password"] = proxy_password
            context_options["proxy"] = proxy_config

        user_data_dir = os.path.join(DATA_DIR, profile_id)
        os.makedirs(user_data_dir, exist_ok=True)

        storage_file = os.path.join(user_data_dir, "storage.json")
        if os.path.exists(storage_file):
            context_options["storage_state"] = storage_file

        context = await self._browser.new_context(**context_options)
        self._contexts[profile_id] = context

        page = await context.new_page()
        await page.goto("about:blank")

    async def stop_profile(self, profile_id: str) -> None:
        """Stop and close a profile's browser context."""
        context = self._contexts.get(profile_id)
        if context is None:
            return

        user_data_dir = os.path.join(DATA_DIR, profile_id)
        os.makedirs(user_data_dir, exist_ok=True)
        storage_file = os.path.join(user_data_dir, "storage.json")
        try:
            await context.storage_state(path=storage_file)
        except Exception:
            pass

        await context.close()
        del self._contexts[profile_id]

    def is_running(self, profile_id: str) -> bool:
        """Check if a profile's browser is currently running."""
        return profile_id in self._contexts

    async def shutdown(self):
        """Close all contexts and the browser."""
        for profile_id in list(self._contexts.keys()):
            await self.stop_profile(profile_id)
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()


# Singleton instance
browser_manager = BrowserManager()
