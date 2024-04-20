import hashlib
import jwt
import redis

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, SECRET_JWT_KEY, REDIS_PASS
from src.database import DBManager

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

redis = redis.Redis(
    host='redis-10905.c239.us-east-1-2.ec2.redns.redis-cloud.com',
    port=10905,
    password=REDIS_PASS)


def save_data(key, value):
    redis.rpush(key, value)
    redis.save()


def get_data(key):
    values = redis.lrange(key, 0, -1)
    redis.ltrim(key, 1, 0)
    int_values = [int(item.decode('utf-8')) for item in values]
    return int_values


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


def create_access_token(uid: int) -> str:
    secrert_key = SECRET_JWT_KEY
    algorithm = "HS256"
    to_encode = {"sub": uid}
    encoded_jwt = jwt.encode(to_encode, secrert_key, algorithm=algorithm)
    return encoded_jwt


def verify_request(token: str, uid: int):
    return create_access_token(uid) == token
