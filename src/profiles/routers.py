import os

import fastapi
from fastapi import status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.profiles.models import Profile
from src.profiles.schemas import ChangeProfileInfo
from src.utils import get_db_manager, verify_request, decode_jwt_token, update_location

router = fastapi.APIRouter()


@router.post("/update_profile", status_code=status.HTTP_200_OK)
async def update_profile(info: ChangeProfileInfo):
    if not verify_request(info.token):
        raise HTTPException(status_code=400, detail="Invalid token")
    try:
        lat, lon = list(map(float, info.new_info.location.split(", ")))
        location = str(lat) + ", " + str(lon)
    except Exception as _:
        raise HTTPException(status_code=400, detail="Invalid location")
    db_manager = await get_db_manager()
    user_id = decode_jwt_token(info.token)['user_id']

    old_location = await db_manager.get_user_location(user_id)
    if old_location != info.new_info.location:
        await update_location(lat, lon, user_id)

    info.new_info.location = location
    await db_manager.update_profile_info(user_id, info.new_info)
    return {"status": "ok"}


@router.get("/get_profile", status_code=status.HTTP_200_OK)
async def get_profile(token: str):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decode_jwt_token(token)['user_id']
    db_manager = await get_db_manager()
    profile = await db_manager.get_profile_by_id(user_id)
    profile = profile._asdict()  # NOQA
    profile.pop("id", None)
    return {"profile": Profile(**profile)}


@router.get("/get_custom_profile_info", status_code=status.HTTP_200_OK)
async def get_profile_by_id(token: str, user_id: int):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    db_manager = await get_db_manager()
    profile = await db_manager.get_profile_by_id(user_id)
    profile = profile._asdict()  # NOQA
    profile.pop("id", None)
    return {"profile": Profile(**profile)}


@router.post("/upload_profile_image", status_code=status.HTTP_200_OK)
async def upload_profile_image(token: str, image: UploadFile = File(...)):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    try:
        user_id = decode_jwt_token(token)['user_id']
        file_name = f"{user_id}_profile_image.jpg"

        directory = "profile_images"
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(f"profile_images/{file_name}", "wb") as file:
            file.write(image.file.read())
    except Exception as ex:
        raise HTTPException(status_code=400, detail=ex)

    return {"status": "ok"}


@router.get("/get_profile_image", status_code=status.HTTP_200_OK)
async def get_profile_image(token: str, profile_id: str):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    return FileResponse(f"profile_images/{profile_id}_profile_image.jpg", media_type="image/jpeg")
