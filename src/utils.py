import hashlib

import jwt
import redis
from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, SECRET_JWT_KEY, REDIS_PASS, ES_CLOUD_PASS
from src.database import DBManager

from math import radians, sin, cos, sqrt, atan2

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# redis = redis.Redis(
#     host='redis-10905.c239.us-east-1-2.ec2.redns.redis-cloud.com',
#     port=10905,
#     password=REDIS_PASS)

redis = redis.Redis(
    host='127.0.0.1',
    port=6379)

es = Elasticsearch("http://localhost:9200")

mapping = {
    "mappings": {
        "properties": {
            "location": {"type": "geo_point"}
        }
    }
}


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


def delete_location(lat: float, lon: float):
    query = {
        "query": {
            "match": {
                "location.lat": lat,
                "location.lon": lon
            }
        }
    }

    es.delete_by_query(index="location", body=query)


def get_all_documents(index_name):
    query = {
        "query": {
            "match_all": {}
        }
    }

    result = es.search(index=index_name, body=query)

    for hit in result["hits"]["hits"]:
        document = hit["_source"]
        print(document)


def calculate_distance(lat1, lon1, lat2, lon2):
    r = 6371.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c
    return distance


def save_data(key, value):
    redis.rpush(key, value)


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


if __name__ == '__main__':
    add_location(-45.123456, 78.456789, 1)
    add_location(12.345678, -98.765432, 2)
    add_location(0.987654, 34.567890, 3)
    add_location(-23.456789, -56.789012, 4)
    add_location(67.890123, 123.456789, 5)



    get_all_documents("location")
