from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class ProxyCheckResult:
    valid: bool
    ip: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    error: Optional[str] = None


async def check_proxy(
    host: str,
    port: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> ProxyCheckResult:
    """Validate a proxy by making a request to ip-api.com through it.

    Returns ProxyCheckResult with IP, location, and timezone info.
    """
    if username and password:
        proxy_url = f"http://{username}:{password}@{host}:{port}"
    else:
        proxy_url = f"http://{host}:{port}"

    try:
        async with httpx.AsyncClient(
            proxy=proxy_url,
            timeout=15.0,
        ) as client:
            response = await client.get("http://ip-api.com/json/")
            data = response.json()

            if data.get("status") == "success":
                return ProxyCheckResult(
                    valid=True,
                    ip=data.get("query"),
                    city=data.get("city"),
                    country=data.get("country"),
                    timezone=data.get("timezone"),
                )
            else:
                return ProxyCheckResult(
                    valid=False,
                    error=data.get("message", "Unknown error from ip-api"),
                )
    except Exception as e:
        return ProxyCheckResult(valid=False, error=str(e))
