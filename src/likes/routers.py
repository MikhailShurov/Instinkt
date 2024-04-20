from fastapi import APIRouter, HTTPException
from fastapi import status
from src.utils import create_access_token, save_data, get_data, verify_request

from src.likes.schemas import Like, GetLikes

router = APIRouter()


@router.post("/like", status_code=status.HTTP_200_OK)
async def like(like_obj: Like):
    if not verify_request(like_obj.initiator_token, like_obj.initiator_id):
        raise HTTPException(status_code=400, detail="Invalid initiator_id or token")

    save_data(like_obj.profile_to_like_id, like_obj.initiator_id)
    return {"status": "ok"}


@router.post("/get_likes", status_code=status.HTTP_200_OK)
async def get_likes(user: GetLikes):
    if not verify_request(user.initiator_token, user.initiator_id):
        raise HTTPException(status_code=400, detail="Invalid initiator_id or token")

    values = get_data(str(user.initiator_id))
    return {"user_ids": values}
