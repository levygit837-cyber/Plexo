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
