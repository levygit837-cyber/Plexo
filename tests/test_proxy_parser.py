from backend.services.proxy_parser import parse_proxy


def test_parse_host_port_user_pass():
    """Webshare format: host:port:user:pass"""
    result = parse_proxy("proxy.example.com:8080:myuser:mypass")
    assert result == {
        "host": "proxy.example.com",
        "port": 8080,
        "username": "myuser",
        "password": "mypass",
    }


def test_parse_user_pass_at_host_port():
    """Format: user:pass@host:port"""
    result = parse_proxy("myuser:mypass@proxy.example.com:8080")
    assert result == {
        "host": "proxy.example.com",
        "port": 8080,
        "username": "myuser",
        "password": "mypass",
    }


def test_parse_host_port_only():
    """Format: host:port (no auth)"""
    result = parse_proxy("proxy.example.com:8080")
    assert result == {
        "host": "proxy.example.com",
        "port": 8080,
        "username": None,
        "password": None,
    }


def test_parse_url_format():
    """Format: http://user:pass@host:port"""
    result = parse_proxy("http://myuser:mypass@proxy.example.com:8080")
    assert result == {
        "host": "proxy.example.com",
        "port": 8080,
        "username": "myuser",
        "password": "mypass",
    }


def test_parse_https_url_format():
    """Format: https://user:pass@host:port"""
    result = parse_proxy("https://myuser:mypass@proxy.example.com:8080")
    assert result == {
        "host": "proxy.example.com",
        "port": 8080,
        "username": "myuser",
        "password": "mypass",
    }


def test_parse_strips_whitespace():
    result = parse_proxy("  proxy.example.com:8080:user:pass  ")
    assert result["host"] == "proxy.example.com"


def test_parse_invalid_returns_none():
    result = parse_proxy("not-a-proxy")
    assert result is None


def test_parse_empty_returns_none():
    result = parse_proxy("")
    assert result is None
