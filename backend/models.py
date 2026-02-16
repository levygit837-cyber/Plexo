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
