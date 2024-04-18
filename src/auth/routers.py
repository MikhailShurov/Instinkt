from fastapi import APIRouter, HTTPException
from fastapi import status

from src.auth.schemas import *
from src.utils import get_db_manager, hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(user_data: UserRegistration):
    db_manager = await get_db_manager()
    user = await db_manager.get_user_by_email(user_data.email)
    if user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    await db_manager.create_user(email=user_data.email, hashed_password=hashed_password)
    await db_manager.create_empty_profile(user_data.email)
    return {"message": "User created successfully"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_data: UserRegistration):
    db_manager = await get_db_manager()
    user = await db_manager.get_user_by_email(user_data.email)
    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(user_data.email)
    return {"access_token": access_token}
