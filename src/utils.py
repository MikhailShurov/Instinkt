import hashlib
import jwt

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, SECRET_JWT_KEY
from src.database import DBManager

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_db_manager() -> DBManager:
    async with async_session_maker() as session:
        return DBManager(session)


def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password


def create_access_token(email: str) -> str:
    secrert_key = SECRET_JWT_KEY
    algorithm = "HS256"
    to_encode = {"sub": email}
    encoded_jwt = jwt.encode(to_encode, secrert_key, algorithm=algorithm)
    return encoded_jwt
