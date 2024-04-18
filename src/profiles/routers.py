import fastapi
from fastapi import status, HTTPException

from src.profiles.models import Profile
from src.profiles.shemas import GetProfileByEmail, ChangeProfileInfo
from src.utils import get_db_manager, create_access_token

router = fastapi.APIRouter()


@router.post("/update_profile", status_code=status.HTTP_200_OK)
async def update_profile(info: ChangeProfileInfo):
    token = create_access_token(info.email)
    if token != info.token:
        raise HTTPException(status_code=400, detail="Invalid email or token")
    info.new_info.email = info.email
    db_manager = await get_db_manager()
    await db_manager.update_profile_info(info.new_info)
    return {"status": "ok"}


@router.post("/get_profile_by_email", status_code=status.HTTP_200_OK)
async def get_profile_by_email(info: GetProfileByEmail):
    token = create_access_token(info.email)
    if token != info.token:
        raise HTTPException(status_code=400, detail="Invalid email or token")
    db_manager = await get_db_manager()
    profile = await db_manager.get_profile_by_email(info.email)
    if profile is None:
        raise HTTPException(status_code=400, detail="No such email")

    profile = profile._asdict()  # NOQA
    return {"profile": Profile(**profile)}
