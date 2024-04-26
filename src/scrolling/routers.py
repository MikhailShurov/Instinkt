from fastapi import APIRouter, status, HTTPException

from src.scrolling.schemas import NearbyProfilesRequest
from src.utils import get_db_manager, verify_request, search_nearby_people, calculate_distance

router = APIRouter()


@router.post("/get_nearby_profiles", status_code=status.HTTP_200_OK)
async def get_nearby_profiles(data: NearbyProfilesRequest):
    db_manager = await get_db_manager()
    if not verify_request(data.token, data.profile_id):
        raise HTTPException(status_code=400, detail="Invalid id or token")

    location = await db_manager.get_location_by_id(data.profile_id)
    result = list(map(float, location.split(", ")))
    lat, lon = result[0], result[1]

    result = search_nearby_people(float(lat), float(lon), data.search_radius)
    result = result['hits']['hits']

    answer = []
    for hit in result:
        if hit['_source']['uid'] != data.profile_id:
            lat2, lon2 = hit['_source']['location']['lat'], hit['_source']['location']['lon']
            distance = round(calculate_distance(lat, lon, lat2, lon2), 2)
            answer.append({'uid': hit['_source']['uid'], 'distance': distance})
    return {'locations': answer}
