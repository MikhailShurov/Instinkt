from fastapi import APIRouter, HTTPException
from fastapi import status

from src.likes.schemas import Like, GetLikes
from src.utils import save_data, get_data, verify_request, get_db_manager

router = APIRouter()


@router.post("/like", status_code=status.HTTP_200_OK)
async def like(like_obj: Like):
    if not verify_request(like_obj.initiator_token, like_obj.initiator_id):
        raise HTTPException(status_code=400, detail="Invalid initiator_id or token")

    save_data(like_obj.profile_to_like_id, like_obj.initiator_id)
    db_manager = await get_db_manager()
    try:
        result = await db_manager.like(like_obj.initiator_id, like_obj.profile_to_like_id)
    except Exception as e:
        print(e)
        return {"status": str(e)}
    return {"status": result}


@router.get("/get_likes", status_code=status.HTTP_200_OK)
async def get_likes(user: GetLikes):
    if not verify_request(user.initiator_token, user.initiator_id):
        raise HTTPException(status_code=400, detail="Invalid initiator_id or token")

    values = get_data(str(user.initiator_id))
    return {"user_ids": values}


@router.post("/get_mutual_likes", status_code=status.HTTP_200_OK)
async def get_mutual_likes(user: GetLikes):
    if not verify_request(user.initiator_token, user.initiator_id):
        raise HTTPException(status_code=400, detail="Invalid initiator_id OR token")

    db_manager = await get_db_manager()
    mutual_likes = await db_manager.get_mutual_likes(user.initiator_id)
    result = [ulike[1] for ulike in mutual_likes]
    return {"mutual_likes": result}
