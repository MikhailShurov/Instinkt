import hashlib

import jwt
import redis
from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, SECRET_JWT_KEY, REDIS_PASS, ES_CLOUD_PASS
from src.database import DBManager

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

redis = redis.Redis(
    host='redis-10905.c239.us-east-1-2.ec2.redns.redis-cloud.com',
    port=10905,
    password=REDIS_PASS)

es = Elasticsearch("https://f768326d7dda43fa91bf11bbc0da454b.us-central1.gcp.cloud.es.io",
                   basic_auth=('elastic', ES_CLOUD_PASS))

mapping = {
        "mappings": {
            "properties": {
                "location": {"type": "geo_point"}
            }
        }
    }
# es.indices.delete(index="location")
# es.indices.create(index="location", body=mapping)


def search_nearby_people(lat: float, lon: float, r: int) -> list:
    index_name = "location"
    query = {
        "query": {
            "bool": {
                "must": {
                    "match_all": {}
                },
                "filter": {
                    "geo_distance": {
                        "distance": f"{r}km",
                        "location": {
                            "lat": lat,
                            "lon": lon
                        }
                    }
                }
            }
        }
    }
    result = es.search(index=index_name, body=query)
    return result


def add_location(lat: float, lon: float, uid: int):
    new_location = {
        "uid": uid,
        "location": {"lat": lat, "lon": lon}
    }

    es.index(index="location", body=new_location)


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
