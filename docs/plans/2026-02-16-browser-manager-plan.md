# Browser Manager Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a simple anti-detect browser profile manager (like Dolphin Anty/GoLogin) with profile creation, proxy management, and isolated Chromium instances.

**Architecture:** Monolith with FastAPI backend serving a React SPA. SQLite for persistence via SQLModel. Playwright controls isolated Chromium instances per profile. Each profile gets its own persistent browser data directory.

**Tech Stack:** Python 3.11+ (FastAPI, SQLModel, Playwright, httpx), React 18 (TypeScript, Vite, Tailwind CSS), SQLite

---

### Task 1: Initialize Project Structure

**Files:**
- Create: `backend/main.py`
- Create: `backend/requirements.txt`
- Create: `backend/__init__.py`
- Create: `backend/routers/__init__.py`
- Create: `backend/services/__init__.py`

**Step 1: Create backend directory structure**

```bash
mkdir -p backend/routers backend/services backend/data/browser_data tests
touch backend/__init__.py backend/routers/__init__.py backend/services/__init__.py
```

**Step 2: Create requirements.txt**

```
# backend/requirements.txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
sqlmodel==0.0.24
httpx==0.28.1
playwright==1.49.1
python-multipart==0.0.20
pytest==8.3.4
pytest-asyncio==0.24.0
```

**Step 3: Create minimal main.py**

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Browser Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
```

**Step 4: Install dependencies and verify**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

**Step 5: Run and verify health endpoint**

Run: `cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000`
Then: `curl http://localhost:8000/api/health`
Expected: `{"status":"ok"}`

**Step 6: Commit**

```bash
git add backend/ tests/
git commit -m "feat: initialize backend project structure with FastAPI"
```

---

### Task 2: Database Models and Setup

**Files:**
- Create: `backend/models.py`
- Create: `backend/database.py`

**Step 1: Write the failing test**

```python
# tests/test_models.py
from sqlmodel import Session, create_engine, SQLModel
from backend.models import Profile


def test_create_profile():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        profile = Profile(
            name="Test Profile",
            user_agent="Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0",
            screen_width=1920,
            screen_height=1080,
            proxy_host="proxy.example.com",
            proxy_port=8080,
            proxy_username="user",
            proxy_password="pass",
            timezone="America/Sao_Paulo",
        )
        session.add(profile)
        session.commit()
        session.refresh(profile)

        assert profile.id is not None
        assert profile.name == "Test Profile"
        assert profile.status == "stopped"
        assert profile.proxy_host == "proxy.example.com"
        assert profile.proxy_port == 8080


def test_profile_without_proxy():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        profile = Profile(name="No Proxy Profile")
        session.add(profile)
        session.commit()
        session.refresh(profile)

        assert profile.id is not None
        assert profile.proxy_host is None
        assert profile.status == "stopped"
```

**Step 2: Run test to verify it fails**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_models.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'backend.models'"

**Step 3: Write the models**

```python
# backend/models.py
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    name: str = Field(index=True)
    user_agent: Optional[str] = Field(default=None)
    screen_width: int = Field(default=1920)
    screen_height: int = Field(default=1080)
    proxy_host: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None)
    proxy_username: Optional[str] = Field(default=None)
    proxy_password: Optional[str] = Field(default=None)
    timezone: Optional[str] = Field(default=None)


class Profile(ProfileBase, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    status: str = Field(default="stopped")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(SQLModel):
    name: Optional[str] = None
    user_agent: Optional[str] = None
    screen_width: Optional[int] = None
    screen_height: Optional[int] = None
    proxy_host: Optional[str] = None
    proxy_port: Optional[int] = None
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None
    timezone: Optional[str] = None


class ProfilePublic(ProfileBase):
    id: str
    status: str
    created_at: datetime
```

**Step 4: Write the database setup**

```python
# backend/database.py
import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'profiles.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
```

**Step 5: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_models.py -v`
Expected: 2 passed

**Step 6: Commit**

```bash
git add backend/models.py backend/database.py tests/test_models.py
git commit -m "feat: add Profile SQLModel and database setup"
```

---

### Task 3: Proxy Parser Service

**Files:**
- Create: `backend/services/proxy_parser.py`
- Create: `tests/test_proxy_parser.py`

**Step 1: Write the failing tests**

```python
# tests/test_proxy_parser.py
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
```

**Step 2: Run tests to verify they fail**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_proxy_parser.py -v`
Expected: FAIL

**Step 3: Implement proxy parser**

```python
# backend/services/proxy_parser.py
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
```

**Step 4: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_proxy_parser.py -v`
Expected: 8 passed

**Step 5: Commit**

```bash
git add backend/services/proxy_parser.py tests/test_proxy_parser.py
git commit -m "feat: add proxy parser with multi-format support"
```

---

### Task 4: Proxy Checker Service

**Files:**
- Create: `backend/services/proxy_checker.py`
- Create: `tests/test_proxy_checker.py`

**Step 1: Write the failing test**

```python
# tests/test_proxy_checker.py
import pytest
from unittest.mock import AsyncMock, patch
from backend.services.proxy_checker import check_proxy, ProxyCheckResult


@pytest.mark.asyncio
async def test_check_proxy_success():
    mock_response = AsyncMock()
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
```

**Step 2: Run tests to verify they fail**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_proxy_checker.py -v`
Expected: FAIL

**Step 3: Implement proxy checker**

```python
# backend/services/proxy_checker.py
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
```

**Step 4: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_proxy_checker.py -v`
Expected: 2 passed

**Step 5: Commit**

```bash
git add backend/services/proxy_checker.py tests/test_proxy_checker.py
git commit -m "feat: add proxy checker service with ip-api.com validation"
```

---

### Task 5: Profiles API Router (CRUD)

**Files:**
- Create: `backend/routers/profiles.py`
- Modify: `backend/main.py`
- Create: `tests/test_profiles_api.py`

**Step 1: Write the failing tests**

```python
# tests/test_profiles_api.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app
from backend.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
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
```

**Step 2: Run tests to verify they fail**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_profiles_api.py -v`
Expected: FAIL

**Step 3: Implement profiles router**

```python
# backend/routers/profiles.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from backend.database import SessionDep
from backend.models import Profile, ProfileCreate, ProfilePublic, ProfileUpdate

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.get("", response_model=list[ProfilePublic])
def list_profiles(session: SessionDep):
    profiles = session.exec(select(Profile)).all()
    return profiles


@router.post("", response_model=ProfilePublic)
def create_profile(profile_data: ProfileCreate, session: SessionDep):
    profile = Profile.model_validate(profile_data)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=ProfilePublic)
def get_profile(profile_id: str, session: SessionDep):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{profile_id}", response_model=ProfilePublic)
def update_profile(
    profile_id: str, profile_data: ProfileUpdate, session: SessionDep
):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    update_dict = profile_data.model_dump(exclude_unset=True)
    profile.sqlmodel_update(update_dict)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.delete("/{profile_id}")
def delete_profile(profile_id: str, session: SessionDep):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    session.delete(profile)
    session.commit()
    return {"ok": True}
```

**Step 4: Update main.py to include router and startup event**

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_db_and_tables
from backend.routers.profiles import router as profiles_router

app = FastAPI(title="Browser Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
```

**Step 5: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_profiles_api.py -v`
Expected: 6 passed

**Step 6: Commit**

```bash
git add backend/routers/profiles.py backend/main.py tests/test_profiles_api.py
git commit -m "feat: add profiles CRUD API endpoints"
```

---

### Task 6: Proxy API Router (Parse + Validate)

**Files:**
- Create: `backend/routers/proxy.py`
- Modify: `backend/main.py`
- Create: `tests/test_proxy_api.py`

**Step 1: Write the failing tests**

```python
# tests/test_proxy_api.py
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
```

**Step 2: Run tests to verify they fail**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_proxy_api.py -v`
Expected: FAIL

**Step 3: Implement proxy router**

```python
# backend/routers/proxy.py
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.proxy_parser import parse_proxy
from backend.services.proxy_checker import check_proxy

router = APIRouter(prefix="/api/proxy", tags=["proxy"])


class ProxyParseRequest(BaseModel):
    raw: str


class ProxyValidateRequest(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None


@router.post("/parse")
def parse_proxy_endpoint(request: ProxyParseRequest):
    result = parse_proxy(request.raw)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Could not parse proxy string. Supported formats: "
            "host:port:user:pass, user:pass@host:port, host:port, "
            "http://user:pass@host:port",
        )
    return result


@router.post("/validate")
async def validate_proxy_endpoint(request: ProxyValidateRequest):
    result = await check_proxy(
        host=request.host,
        port=request.port,
        username=request.username,
        password=request.password,
    )
    return {
        "valid": result.valid,
        "ip": result.ip,
        "city": result.city,
        "country": result.country,
        "timezone": result.timezone,
        "error": result.error,
    }
```

**Step 4: Add proxy router to main.py**

Add to `backend/main.py` after profiles_router:

```python
from backend.routers.proxy import router as proxy_router
app.include_router(proxy_router)
```

**Step 5: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_proxy_api.py -v`
Expected: 3 passed

**Step 6: Commit**

```bash
git add backend/routers/proxy.py backend/main.py tests/test_proxy_api.py
git commit -m "feat: add proxy parse and validate API endpoints"
```

---

### Task 7: Browser Manager Service

**Files:**
- Create: `backend/services/browser.py`
- Create: `tests/test_browser_service.py`

**Step 1: Write the failing test**

```python
# tests/test_browser_service.py
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
```

**Step 2: Run tests to verify they fail**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_browser_service.py -v`
Expected: FAIL

**Step 3: Implement browser manager**

```python
# backend/services/browser.py
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
```

**Step 4: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_browser_service.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add backend/services/browser.py tests/test_browser_service.py
git commit -m "feat: add browser manager service with Playwright"
```

---

### Task 8: Profile Start/Stop API Endpoints

**Files:**
- Modify: `backend/routers/profiles.py`
- Modify: `tests/test_profiles_api.py`

**Step 1: Write the failing tests**

Add to `tests/test_profiles_api.py`:

```python
from unittest.mock import patch, AsyncMock


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
```

**Step 2: Run tests to verify they fail**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_profiles_api.py::test_start_profile tests/test_profiles_api.py::test_stop_profile -v`
Expected: FAIL

**Step 3: Add start/stop endpoints to profiles router**

Add to `backend/routers/profiles.py`:

```python
from backend.services.browser import browser_manager


@router.post("/{profile_id}/start", response_model=ProfilePublic)
async def start_profile(profile_id: str, session: SessionDep):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    await browser_manager.start_profile(
        profile_id=profile.id,
        proxy_host=profile.proxy_host,
        proxy_port=profile.proxy_port,
        proxy_username=profile.proxy_username,
        proxy_password=profile.proxy_password,
        user_agent=profile.user_agent,
        screen_width=profile.screen_width,
        screen_height=profile.screen_height,
        timezone=profile.timezone,
    )

    profile.status = "running"
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.post("/{profile_id}/stop", response_model=ProfilePublic)
async def stop_profile(profile_id: str, session: SessionDep):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    await browser_manager.stop_profile(profile_id)

    profile.status = "stopped"
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
```

**Step 4: Run tests to verify they pass**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/test_profiles_api.py -v`
Expected: 8 passed

**Step 5: Commit**

```bash
git add backend/routers/profiles.py tests/test_profiles_api.py
git commit -m "feat: add profile start/stop browser endpoints"
```

---

### Task 9: Initialize React Frontend

**Files:**
- Create: `frontend/` directory (via Vite)
- Create: `frontend/src/lib/api.ts`

**Step 1: Scaffold React + TypeScript + Vite project**

```bash
cd /home/levybonito
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss @tailwindcss/vite
```

**Step 2: Configure Tailwind with Vite**

Replace `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
```

Replace `frontend/src/index.css`:

```css
@import "tailwindcss";
```

**Step 3: Create API client**

```typescript
// frontend/src/lib/api.ts
const BASE_URL = "/api";

export interface Profile {
  id: string;
  name: string;
  user_agent: string | null;
  screen_width: number;
  screen_height: number;
  proxy_host: string | null;
  proxy_port: number | null;
  proxy_username: string | null;
  proxy_password: string | null;
  timezone: string | null;
  status: "stopped" | "running";
  created_at: string;
}

export interface ProfileCreate {
  name: string;
  user_agent?: string;
  screen_width?: number;
  screen_height?: number;
  proxy_host?: string;
  proxy_port?: number;
  proxy_username?: string;
  proxy_password?: string;
  timezone?: string;
}

export interface ProxyCheckResult {
  valid: boolean;
  ip: string | null;
  city: string | null;
  country: string | null;
  timezone: string | null;
  error: string | null;
}

export interface ParsedProxy {
  host: string;
  port: number;
  username: string | null;
  password: string | null;
}

export async function fetchProfiles(): Promise<Profile[]> {
  const res = await fetch(`${BASE_URL}/profiles`);
  return res.json();
}

export async function createProfile(data: ProfileCreate): Promise<Profile> {
  const res = await fetch(`${BASE_URL}/profiles`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function deleteProfile(id: string): Promise<void> {
  await fetch(`${BASE_URL}/profiles/${id}`, { method: "DELETE" });
}

export async function startProfile(id: string): Promise<Profile> {
  const res = await fetch(`${BASE_URL}/profiles/${id}/start`, {
    method: "POST",
  });
  return res.json();
}

export async function stopProfile(id: string): Promise<Profile> {
  const res = await fetch(`${BASE_URL}/profiles/${id}/stop`, {
    method: "POST",
  });
  return res.json();
}

export async function parseProxy(raw: string): Promise<ParsedProxy> {
  const res = await fetch(`${BASE_URL}/proxy/parse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ raw }),
  });
  if (!res.ok) throw new Error("Failed to parse proxy");
  return res.json();
}

export async function validateProxy(data: {
  host: string;
  port: number;
  username?: string;
  password?: string;
}): Promise<ProxyCheckResult> {
  const res = await fetch(`${BASE_URL}/proxy/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
```

**Step 4: Verify dev server starts**

Run: `cd /home/levybonito/frontend && npm run dev`
Expected: Vite dev server running on http://localhost:5173

**Step 5: Commit**

```bash
git add frontend/
git commit -m "feat: initialize React + Vite + Tailwind frontend with API client"
```

---

### Task 10: Profile List Component

**Files:**
- Create: `frontend/src/hooks/useProfiles.ts`
- Create: `frontend/src/components/ProfileCard.tsx`
- Create: `frontend/src/components/ProfileList.tsx`
- Modify: `frontend/src/App.tsx`

**Step 1: Create useProfiles hook**

```typescript
// frontend/src/hooks/useProfiles.ts
import { useCallback, useEffect, useState } from "react";
import {
  fetchProfiles,
  createProfile,
  deleteProfile,
  startProfile,
  stopProfile,
  type Profile,
  type ProfileCreate,
} from "../lib/api";

export function useProfiles() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchProfiles();
      setProfiles(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const create = async (data: ProfileCreate) => {
    const profile = await createProfile(data);
    setProfiles((prev) => [...prev, profile]);
    return profile;
  };

  const remove = async (id: string) => {
    await deleteProfile(id);
    setProfiles((prev) => prev.filter((p) => p.id !== id));
  };

  const start = async (id: string) => {
    const updated = await startProfile(id);
    setProfiles((prev) => prev.map((p) => (p.id === id ? updated : p)));
  };

  const stop = async (id: string) => {
    const updated = await stopProfile(id);
    setProfiles((prev) => prev.map((p) => (p.id === id ? updated : p)));
  };

  return { profiles, loading, refresh, create, remove, start, stop };
}
```

**Step 2: Create ProfileCard component**

```tsx
// frontend/src/components/ProfileCard.tsx
import type { Profile } from "../lib/api";

interface ProfileCardProps {
  profile: Profile;
  onStart: (id: string) => void;
  onStop: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ProfileCard({
  profile,
  onStart,
  onStop,
  onDelete,
}: ProfileCardProps) {
  const isRunning = profile.status === "running";

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{profile.name}</h3>
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${
            isRunning
              ? "bg-emerald-500/10 text-emerald-400"
              : "bg-zinc-700/50 text-zinc-400"
          }`}
        >
          <span
            className={`w-1.5 h-1.5 rounded-full ${
              isRunning ? "bg-emerald-400" : "bg-zinc-500"
            }`}
          />
          {isRunning ? "Rodando" : "Parado"}
        </span>
      </div>

      <div className="text-sm text-zinc-400 space-y-1">
        {profile.proxy_host && (
          <p>
            Proxy: {profile.proxy_host}:{profile.proxy_port}
          </p>
        )}
        <p>
          Tela: {profile.screen_width}x{profile.screen_height}
        </p>
        {profile.timezone && <p>Timezone: {profile.timezone}</p>}
      </div>

      <div className="flex gap-2 mt-auto pt-2">
        {isRunning ? (
          <button
            onClick={() => onStop(profile.id)}
            className="flex-1 px-3 py-2 bg-red-500/10 text-red-400 rounded-lg text-sm font-medium hover:bg-red-500/20 transition-colors cursor-pointer"
          >
            Parar
          </button>
        ) : (
          <button
            onClick={() => onStart(profile.id)}
            className="flex-1 px-3 py-2 bg-emerald-500/10 text-emerald-400 rounded-lg text-sm font-medium hover:bg-emerald-500/20 transition-colors cursor-pointer"
          >
            Abrir
          </button>
        )}
        <button
          onClick={() => onDelete(profile.id)}
          disabled={isRunning}
          className="px-3 py-2 bg-zinc-800 text-zinc-400 rounded-lg text-sm font-medium hover:bg-zinc-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          Deletar
        </button>
      </div>
    </div>
  );
}
```

**Step 3: Create ProfileList component**

```tsx
// frontend/src/components/ProfileList.tsx
import type { Profile } from "../lib/api";
import { ProfileCard } from "./ProfileCard";

interface ProfileListProps {
  profiles: Profile[];
  loading: boolean;
  onStart: (id: string) => void;
  onStop: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ProfileList({
  profiles,
  loading,
  onStart,
  onStop,
  onDelete,
}: ProfileListProps) {
  if (loading) {
    return (
      <div className="text-center text-zinc-500 py-12">Carregando...</div>
    );
  }

  if (profiles.length === 0) {
    return (
      <div className="text-center text-zinc-500 py-12">
        <p className="text-lg">Nenhum perfil criado</p>
        <p className="text-sm mt-1">
          Clique em "Criar Perfil" para comecar
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {profiles.map((profile) => (
        <ProfileCard
          key={profile.id}
          profile={profile}
          onStart={onStart}
          onStop={onStop}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
```

**Step 4: Update App.tsx**

```tsx
// frontend/src/App.tsx
import { useState } from "react";
import { ProfileList } from "./components/ProfileList";
import { useProfiles } from "./hooks/useProfiles";

function App() {
  const { profiles, loading, create, remove, start, stop } = useProfiles();
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold">Browser Manager</h1>
          <button
            onClick={() => setShowCreate(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-500 transition-colors cursor-pointer"
          >
            + Criar Perfil
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <ProfileList
          profiles={profiles}
          loading={loading}
          onStart={start}
          onStop={stop}
          onDelete={remove}
        />
      </main>
    </div>
  );
}

export default App;
```

**Step 5: Verify frontend renders**

Run backend: `uvicorn backend.main:app --reload --port 8000`
Run frontend: `cd frontend && npm run dev`
Open: http://localhost:5173
Expected: Dark page with "Browser Manager" header and empty state

**Step 6: Commit**

```bash
git add frontend/src/
git commit -m "feat: add profile list UI with cards and status badges"
```

---

### Task 11: Create Profile Modal with Proxy Input

**Files:**
- Create: `frontend/src/lib/proxyParser.ts`
- Create: `frontend/src/components/ProxyInput.tsx`
- Create: `frontend/src/components/ProxyStatus.tsx`
- Create: `frontend/src/components/CreateProfileModal.tsx`
- Modify: `frontend/src/App.tsx`

**Step 1: Create frontend proxy parser**

```typescript
// frontend/src/lib/proxyParser.ts
export interface ParsedProxy {
  host: string;
  port: number;
  username: string | null;
  password: string | null;
}

export function parseProxy(raw: string): ParsedProxy | null {
  const trimmed = raw.trim();
  if (!trimmed) return null;

  // Format: http(s)://user:pass@host:port
  const urlMatch = trimmed.match(
    /^https?:\/\/([^:]+):([^@]+)@([^:]+):(\d+)$/
  );
  if (urlMatch) {
    return {
      host: urlMatch[3],
      port: parseInt(urlMatch[4]),
      username: urlMatch[1],
      password: urlMatch[2],
    };
  }

  // Format: user:pass@host:port
  const atMatch = trimmed.match(/^([^:]+):([^@]+)@([^:]+):(\d+)$/);
  if (atMatch) {
    return {
      host: atMatch[3],
      port: parseInt(atMatch[4]),
      username: atMatch[1],
      password: atMatch[2],
    };
  }

  const parts = trimmed.split(":");

  // Format: host:port:user:pass
  if (parts.length === 4) {
    const port = parseInt(parts[1]);
    if (!isNaN(port)) {
      return {
        host: parts[0],
        port,
        username: parts[2],
        password: parts[3],
      };
    }
  }

  // Format: host:port
  if (parts.length === 2) {
    const port = parseInt(parts[1]);
    if (!isNaN(port)) {
      return { host: parts[0], port, username: null, password: null };
    }
  }

  return null;
}
```

**Step 2: Create ProxyStatus component**

```tsx
// frontend/src/components/ProxyStatus.tsx
import type { ProxyCheckResult } from "../lib/api";

interface ProxyStatusProps {
  result: ProxyCheckResult | null;
  loading: boolean;
}

export function ProxyStatus({ result, loading }: ProxyStatusProps) {
  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-zinc-800 rounded-lg text-sm text-zinc-400">
        <div className="w-4 h-4 border-2 border-zinc-500 border-t-blue-400 rounded-full animate-spin" />
        Verificando proxy...
      </div>
    );
  }

  if (!result) return null;

  if (result.valid) {
    return (
      <div className="px-3 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-sm">
        <div className="flex items-center gap-2 text-emerald-400 font-medium">
          <span>Proxy valida</span>
        </div>
        <div className="text-zinc-400 mt-1 space-y-0.5">
          <p>IP: {result.ip}</p>
          <p>
            Local: {result.city}, {result.country}
          </p>
          <p>Timezone: {result.timezone}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-sm">
      <div className="flex items-center gap-2 text-red-400 font-medium">
        <span>Proxy invalida</span>
      </div>
      {result.error && (
        <p className="text-zinc-400 mt-1">{result.error}</p>
      )}
    </div>
  );
}
```

**Step 3: Create ProxyInput component**

```tsx
// frontend/src/components/ProxyInput.tsx
import { useState, useCallback } from "react";
import { parseProxy } from "../lib/proxyParser";
import { validateProxy, type ProxyCheckResult } from "../lib/api";
import { ProxyStatus } from "./ProxyStatus";

interface ProxyInputProps {
  onProxyChange: (data: {
    host: string;
    port: number;
    username: string | null;
    password: string | null;
  }) => void;
  onTimezoneDetected: (timezone: string) => void;
}

export function ProxyInput({
  onProxyChange,
  onTimezoneDetected,
}: ProxyInputProps) {
  const [rawProxy, setRawProxy] = useState("");
  const [parsedHost, setParsedHost] = useState("");
  const [parsedPort, setParsedPort] = useState("");
  const [parsedUser, setParsedUser] = useState("");
  const [parsedPass, setParsedPass] = useState("");
  const [checkResult, setCheckResult] = useState<ProxyCheckResult | null>(
    null
  );
  const [checking, setChecking] = useState(false);

  const handlePaste = useCallback(
    (e: React.ClipboardEvent<HTMLInputElement>) => {
      const text = e.clipboardData.getData("text");
      const parsed = parseProxy(text);
      if (parsed) {
        e.preventDefault();
        setRawProxy(text.trim());
        setParsedHost(parsed.host);
        setParsedPort(String(parsed.port));
        setParsedUser(parsed.username || "");
        setParsedPass(parsed.password || "");
        setCheckResult(null);
        onProxyChange(parsed);
      }
    },
    [onProxyChange]
  );

  const handleCheck = async () => {
    if (!parsedHost || !parsedPort) return;
    setChecking(true);
    setCheckResult(null);
    try {
      const result = await validateProxy({
        host: parsedHost,
        port: parseInt(parsedPort),
        username: parsedUser || undefined,
        password: parsedPass || undefined,
      });
      setCheckResult(result);
      if (result.valid && result.timezone) {
        onTimezoneDetected(result.timezone);
      }
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="space-y-3">
      <div>
        <label className="block text-sm font-medium text-zinc-300 mb-1">
          Proxy (cole com Ctrl+V)
        </label>
        <input
          type="text"
          value={rawProxy}
          onChange={(e) => setRawProxy(e.target.value)}
          onPaste={handlePaste}
          placeholder="host:port:user:pass"
          className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      {parsedHost && (
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs text-zinc-500 mb-1">Host</label>
            <input
              type="text"
              value={parsedHost}
              onChange={(e) => {
                setParsedHost(e.target.value);
                onProxyChange({
                  host: e.target.value,
                  port: parseInt(parsedPort) || 0,
                  username: parsedUser || null,
                  password: parsedPass || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500 mb-1">Porta</label>
            <input
              type="text"
              value={parsedPort}
              onChange={(e) => {
                setParsedPort(e.target.value);
                onProxyChange({
                  host: parsedHost,
                  port: parseInt(e.target.value) || 0,
                  username: parsedUser || null,
                  password: parsedPass || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500 mb-1">
              Usuario
            </label>
            <input
              type="text"
              value={parsedUser}
              onChange={(e) => {
                setParsedUser(e.target.value);
                onProxyChange({
                  host: parsedHost,
                  port: parseInt(parsedPort) || 0,
                  username: e.target.value || null,
                  password: parsedPass || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500 mb-1">Senha</label>
            <input
              type="text"
              value={parsedPass}
              onChange={(e) => {
                setParsedPass(e.target.value);
                onProxyChange({
                  host: parsedHost,
                  port: parseInt(parsedPort) || 0,
                  username: parsedUser || null,
                  password: e.target.value || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
        </div>
      )}

      {parsedHost && (
        <button
          onClick={handleCheck}
          disabled={checking}
          className="w-full px-3 py-2 bg-zinc-800 text-zinc-300 rounded-lg text-sm font-medium hover:bg-zinc-700 transition-colors disabled:opacity-50 cursor-pointer"
        >
          {checking ? "Verificando..." : "Verificar Proxy"}
        </button>
      )}

      <ProxyStatus result={checkResult} loading={checking} />
    </div>
  );
}
```

**Step 4: Create CreateProfileModal**

```tsx
// frontend/src/components/CreateProfileModal.tsx
import { useState } from "react";
import { ProxyInput } from "./ProxyInput";
import type { ProfileCreate } from "../lib/api";

const USER_AGENTS = [
  {
    label: "Chrome 120 - Windows 10",
    value:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  },
  {
    label: "Chrome 120 - macOS",
    value:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  },
  {
    label: "Chrome 120 - Linux",
    value:
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  },
  {
    label: "Firefox 121 - Windows",
    value:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  },
  {
    label: "Firefox 121 - Linux",
    value:
      "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
  },
];

const RESOLUTIONS = [
  { label: "1920x1080 (Full HD)", width: 1920, height: 1080 },
  { label: "1366x768", width: 1366, height: 768 },
  { label: "1440x900", width: 1440, height: 900 },
  { label: "1536x864", width: 1536, height: 864 },
  { label: "2560x1440 (2K)", width: 2560, height: 1440 },
];

interface CreateProfileModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (data: ProfileCreate) => Promise<void>;
}

export function CreateProfileModal({
  open,
  onClose,
  onCreate,
}: CreateProfileModalProps) {
  const [name, setName] = useState("");
  const [userAgent, setUserAgent] = useState(USER_AGENTS[0].value);
  const [customUA, setCustomUA] = useState("");
  const [useCustomUA, setUseCustomUA] = useState(false);
  const [resolution, setResolution] = useState(0);
  const [proxyData, setProxyData] = useState<{
    host: string;
    port: number;
    username: string | null;
    password: string | null;
  } | null>(null);
  const [timezone, setTimezone] = useState("");
  const [creating, setCreating] = useState(false);

  if (!open) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setCreating(true);
    try {
      const selectedRes = RESOLUTIONS[resolution];
      await onCreate({
        name: name.trim(),
        user_agent: useCustomUA ? customUA : userAgent,
        screen_width: selectedRes.width,
        screen_height: selectedRes.height,
        proxy_host: proxyData?.host,
        proxy_port: proxyData?.port,
        proxy_username: proxyData?.username ?? undefined,
        proxy_password: proxyData?.password ?? undefined,
        timezone: timezone || undefined,
      });
      setName("");
      setProxyData(null);
      setTimezone("");
      onClose();
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800">
          <h2 className="text-lg font-semibold text-white">Criar Perfil</h2>
          <button
            onClick={onClose}
            className="text-zinc-500 hover:text-white transition-colors cursor-pointer text-xl"
          >
            X
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Nome do Perfil
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Meu Perfil"
              required
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              User-Agent
            </label>
            {!useCustomUA ? (
              <select
                value={userAgent}
                onChange={(e) => setUserAgent(e.target.value)}
                className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                {USER_AGENTS.map((ua) => (
                  <option key={ua.value} value={ua.value}>
                    {ua.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={customUA}
                onChange={(e) => setCustomUA(e.target.value)}
                placeholder="Mozilla/5.0 ..."
                className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
              />
            )}
            <button
              type="button"
              onClick={() => setUseCustomUA(!useCustomUA)}
              className="mt-1 text-xs text-blue-400 hover:text-blue-300 cursor-pointer"
            >
              {useCustomUA ? "Usar lista" : "Customizar"}
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Resolucao de Tela
            </label>
            <select
              value={resolution}
              onChange={(e) => setResolution(Number(e.target.value))}
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              {RESOLUTIONS.map((res, i) => (
                <option key={res.label} value={i}>
                  {res.label}
                </option>
              ))}
            </select>
          </div>

          <ProxyInput
            onProxyChange={setProxyData}
            onTimezoneDetected={setTimezone}
          />

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Timezone{" "}
              <span className="text-zinc-500">(auto-detectado pela proxy)</span>
            </label>
            <input
              type="text"
              value={timezone}
              onChange={(e) => setTimezone(e.target.value)}
              placeholder="America/Sao_Paulo"
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2.5 bg-zinc-800 text-zinc-300 rounded-lg font-medium hover:bg-zinc-700 transition-colors cursor-pointer"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={creating || !name.trim()}
              className="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-500 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {creating ? "Criando..." : "Criar Perfil"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

**Step 5: Update App.tsx to include modal**

```tsx
// frontend/src/App.tsx
import { useState } from "react";
import { ProfileList } from "./components/ProfileList";
import { CreateProfileModal } from "./components/CreateProfileModal";
import { useProfiles } from "./hooks/useProfiles";

function App() {
  const { profiles, loading, create, remove, start, stop } = useProfiles();
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold">Browser Manager</h1>
          <button
            onClick={() => setShowCreate(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-500 transition-colors cursor-pointer"
          >
            + Criar Perfil
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <ProfileList
          profiles={profiles}
          loading={loading}
          onStart={start}
          onStop={stop}
          onDelete={remove}
        />
      </main>

      <CreateProfileModal
        open={showCreate}
        onClose={() => setShowCreate(false)}
        onCreate={async (data) => {
          await create(data);
        }}
      />
    </div>
  );
}

export default App;
```

**Step 6: Verify full UI works end-to-end**

Run backend and frontend, test:
1. Click "Criar Perfil" - modal opens
2. Fill name, select user-agent, select resolution
3. Paste a proxy string - fields auto-fill
4. Click "Verificar Proxy" - shows result
5. Click "Criar Perfil" - profile appears in list

**Step 7: Commit**

```bash
git add frontend/src/
git commit -m "feat: add create profile modal with smart proxy input and validator"
```

---

### Task 12: Build Frontend for Production and Serve from FastAPI

**Files:**
- Modify: `backend/main.py`

**Step 1: Build frontend**

```bash
cd /home/levybonito/frontend && npm run build
```

**Step 2: Update main.py to serve the built React app**

Add to `backend/main.py` after all routers:

```python
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(frontend_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dir, "index.html"))
```

**Step 3: Verify production build works**

Run: `cd /home/levybonito && source backend/venv/bin/activate && uvicorn backend.main:app --port 8000`
Open: http://localhost:8000
Expected: Full app running from single server

**Step 4: Commit**

```bash
git add backend/main.py
git commit -m "feat: serve React production build from FastAPI"
```

---

### Task 13: Add Shutdown Hook and Final Polish

**Files:**
- Modify: `backend/main.py`

**Step 1: Add shutdown event to close browsers**

Add to `backend/main.py`:

```python
from backend.services.browser import browser_manager

@app.on_event("shutdown")
async def on_shutdown():
    await browser_manager.shutdown()
```

**Step 2: Run all tests**

Run: `cd /home/levybonito && source backend/venv/bin/activate && python -m pytest tests/ -v`
Expected: All tests pass

**Step 3: Final commit**

```bash
git add backend/main.py
git commit -m "feat: add graceful shutdown for browser manager"
```

---

## Summary

| Task | Component | Description |
|------|-----------|-------------|
| 1 | Setup | Project structure + FastAPI + deps |
| 2 | Backend | SQLModel Profile model + database |
| 3 | Backend | Proxy parser (multi-format) |
| 4 | Backend | Proxy checker (ip-api.com) |
| 5 | Backend | Profiles CRUD API |
| 6 | Backend | Proxy parse + validate API |
| 7 | Backend | Browser manager (Playwright) |
| 8 | Backend | Profile start/stop endpoints |
| 9 | Frontend | React + Vite + Tailwind setup |
| 10 | Frontend | Profile list + cards |
| 11 | Frontend | Create profile modal + proxy input |
| 12 | Deploy | Build frontend + serve from FastAPI |
| 13 | Polish | Shutdown hooks + final tests |
