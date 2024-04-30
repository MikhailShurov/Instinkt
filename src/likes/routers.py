from fastapi import APIRouter, HTTPException
from fastapi import status

from src.likes.schemas import Like
from src.utils import save_data, get_data, verify_request, get_db_manager, decode_jwt_token

router = APIRouter()


@router.post("/like", status_code=status.HTTP_200_OK)
async def like(like_obj: Like):
    if not verify_request(like_obj.token):
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decode_jwt_token(like_obj.token)['user_id']
    save_data(like_obj.profile_to_like_id, user_id)
    db_manager = await get_db_manager()
    try:
        like_exists = await db_manager.check_if_like_exists(user_id)
        if not like_exists:
            result = await db_manager.like(user_id, like_obj.profile_to_like_id)
        else:
            result = "like already exists"
    except Exception as e:
        print(e)
        return {"status": str(e)}
    return {"status": result}


@router.get("/who_likes_me", status_code=status.HTTP_200_OK)
async def get_likes(token: str):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decode_jwt_token(token)['user_id']
    values = get_data(str(user_id))
    return {"user_ids": values}


@router.get("/get_mutual_likes", status_code=status.HTTP_200_OK)
async def get_mutual_likes(token: str):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decode_jwt_token(token)['user_id']
    db_manager = await get_db_manager()
    mutual_likes = await db_manager.get_mutual_likes(user_id)
    result = [ulike[1] for ulike in mutual_likes]
    return {"mutual_likes": result}
