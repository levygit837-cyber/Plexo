import re
from typing import Optional


def parse_proxy(raw: str) -> Optional[dict]:
    """Parse proxy string in multiple formats.

    Supported formats:
    - host:port:user:pass (Webshare)
    - user:pass@host:port
    - host:port
    - http://user:pass@host:port
    - https://user:pass@host:port

    Returns dict with host, port, username, password or None if invalid.
    """
    if not raw or not raw.strip():
        return None

    raw = raw.strip()

    # Format: http(s)://user:pass@host:port
    url_match = re.match(
        r"^https?://([^:]+):([^@]+)@([^:]+):(\d+)$", raw
    )
    if url_match:
        return {
            "host": url_match.group(3),
            "port": int(url_match.group(4)),
            "username": url_match.group(1),
            "password": url_match.group(2),
        }

    # Format: user:pass@host:port
    at_match = re.match(r"^([^:]+):([^@]+)@([^:]+):(\d+)$", raw)
    if at_match:
        return {
            "host": at_match.group(3),
            "port": int(at_match.group(4)),
            "username": at_match.group(1),
            "password": at_match.group(2),
        }

    parts = raw.split(":")

    # Format: host:port:user:pass
    if len(parts) == 4:
        try:
            return {
                "host": parts[0],
                "port": int(parts[1]),
                "username": parts[2],
                "password": parts[3],
            }
        except ValueError:
            return None

    # Format: host:port
    if len(parts) == 2:
        try:
            return {
                "host": parts[0],
                "port": int(parts[1]),
                "username": None,
                "password": None,
            }
        except ValueError:
            return None

    return None
