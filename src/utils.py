import hashlib
from math import radians, sin, cos, sqrt, atan2

import jwt
import redis
from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, SECRET_JWT_KEY, ES_PASS, REDIS_PORT, ES_PORT, DB_PORT
from src.database import DBManager

DATABASE_URL = f"postgresql+asyncpg://{DB_NAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_USER}?async_fallback=True"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # NOQA

redis = redis.Redis(
    host='redis',
    port=REDIS_PORT)

es = Elasticsearch(f"http://elasticsearch:{ES_PORT}", basic_auth=('elastic', ES_PASS))

mapping = {
    "mappings": {
        "properties": {
            "location": {"type": "geo_point"}
        }
    }
}


# es.indices.delete(index=index_name)


async def search_nearby_people(lat: float, lon: float, r: int, size: int) -> list:
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
        },
        "size": size
    }
    result = es.search(index=index_name, body=query)
    return result


async def update_location(lat: float, lon: float, uid: int):
    query = {
        "script": {
            "source": "ctx._source.location.lat = params.lat; ctx._source.location.lon = params.lon",
            "lang": "painless",
            "params": {
                "lat": lat,
                "lon": lon
            }
        }
    }
    es.update_by_query(index="location", body={"query": {"term": {"uid": uid}}, **query})


async def create_base_location(uid: int):
    try:
        es.indices.create(index="location", body=mapping)
    except Exception as _:
        pass
    new_location = {
        "uid": uid,
        "location": {"lat": 0.000000, "lon": 0.000000}
    }

    es.index(index="location", body=new_location)


async def delete_location(lat: float, lon: float):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"location.lat": lat}},
                    {"match": {"location.lon": lon}}
                ]
            }
        }
    }

    es.delete_by_query(index="location", body=query)


async def show_elastic(index_name):
    query = {
        "query": {
            "match_all": {}
        }
    }

    result = es.search(index=index_name, body=query)

    for hit in result["hits"]["hits"]:
        document = hit["_source"]
        print(document)


def clear_index(index_name: str):
    query = {
        "query": {
            "match_all": {}
        }
    }
    es.delete_by_query(index=index_name, body=query)


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


def verify_request(token: str):
    try:
        decode_jwt_token(token)
        return True
    except jwt.InvalidTokenError:
        return False


def create_jwt_token(user_id: int) -> str:
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_JWT_KEY, algorithm="HS256")
    return token


def decode_jwt_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=["HS256"])
    return payload

# async def main():
#     await show_elastic("location")
#
# if __name__ == '__main__':
#     asyncio.run(main())
