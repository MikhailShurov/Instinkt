import fastapi
from fastapi import status, HTTPException

from src.profiles.models import Profile
from src.profiles.schemas import GetProfileByID, ChangeProfileInfo
from src.utils import get_db_manager, create_access_token, verify_request, decode_jwt_token

router = fastapi.APIRouter()


@router.post("/update_profile", status_code=status.HTTP_200_OK)
async def update_profile(info: ChangeProfileInfo):
    if not verify_request(info.token):
        raise HTTPException(status_code=400, detail="Invalid token")
    try:
        lat, lon = list(map(float, info.new_info.location.split(", ")))
        location = str(lat) + ", " + str(lon)
        info.new_info.location = location
    except Exception as _:
        raise HTTPException(status_code=400, detail="Invalid location")
    db_manager = await get_db_manager()
    user_id = decode_jwt_token(info.token)['user_id']
    await db_manager.update_profile_info(user_id, info.new_info)
    return {"status": "ok"}


@router.get("/get_profile_info", status_code=status.HTTP_200_OK)
async def get_profile_by_id(token: str, user_id: int):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    db_manager = await get_db_manager()
    profile = await db_manager.get_profile_by_id(user_id)
    profile = profile._asdict()  # NOQA
    return {"profile": Profile(**profile)}
