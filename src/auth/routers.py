from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from src.auth.schemas import *
from src.utils import get_db_manager, hash_password, verify_password, create_jwt_token, decode_jwt_token, verify_request

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(user_data: UserRegistration):
    db_manager = await get_db_manager()
    user = await db_manager.get_user_by_email(user_data.email)

    if user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    user_id = await db_manager.create_user(email=user_data.email, hashed_password=hashed_password)
    await db_manager.create_empty_profile(user_data.email)
    token = create_jwt_token(user_id)
    return {"message": "User created successfully", "token": token}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_data: UserRegistration):
    db_manager = await get_db_manager()
    user = await db_manager.get_user_by_email(user_data.email)
    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_jwt_token(user.id)
    return {"access_token": access_token}


@router.post("/set_prime_status", status_code=status.HTTP_200_OK)
async def set_prime_status(user_info: UpdatePrimeStatus):
    if not verify_request(user_info.token):
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decode_jwt_token(user_info.token)['user_id']
    db_manager = await get_db_manager()
    await db_manager.update_prime_status(user_id, user_info.prime)
    return {"message": "ok"}


@router.get("/check_prime_status", status_code=status.HTTP_200_OK)
async def set_prime_status(token: str):
    if not verify_request(token):
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decode_jwt_token(token)['user_id']
    db_manager = await get_db_manager()
    result = await db_manager.check_prime_status(user_id)
    return {"prime_status": result}
