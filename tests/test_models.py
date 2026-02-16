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
