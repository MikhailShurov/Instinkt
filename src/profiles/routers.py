import fastapi
from fastapi import status, HTTPException

from src.profiles.models import Profile
from src.profiles.shemas import GetProfileByID, ChangeProfileInfo
from src.utils import get_db_manager, create_access_token

router = fastapi.APIRouter()


@router.post("/update_profile", status_code=status.HTTP_200_OK)
async def update_profile(info: ChangeProfileInfo):
    token = create_access_token(info.id)
    if token != info.token:
        raise HTTPException(status_code=400, detail="Invalid email or token")

    db_manager = await get_db_manager()
    await db_manager.update_profile_info(info.new_info)
    return {"status": "ok"}


@router.get("/get_profile_info", status_code=status.HTTP_200_OK)
async def get_profile_by_id(info: GetProfileByID):
    """
    This endpoint takes user token and user id and returns the profile of this user
    """
    token = create_access_token(info.id)
    if token != info.token:
        raise HTTPException(status_code=400, detail="Invalid email or token")
    db_manager = await get_db_manager()
    profile = await db_manager.get_profile_by_id(info.id)
    if profile is None:
        raise HTTPException(status_code=400, detail="No such email")

    profile = profile._asdict()  # NOQA
    return {"profile": Profile(**profile)}
