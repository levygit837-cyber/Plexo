from fastapi import APIRouter, HTTPException
from sqlmodel import select

from backend.database import SessionDep
from backend.models import Profile, ProfileCreate, ProfilePublic, ProfileUpdate
from backend.services.browser import browser_manager

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
