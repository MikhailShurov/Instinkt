from fastapi import APIRouter, status, HTTPException
from src.utils import get_db_manager, verify_request, add_location, search_nearby_people
from src.scrolling.schemas import NearbyProfilesRequest
router = APIRouter()


@router.post("/get_nearby_profiles", status_code=status.HTTP_200_OK)
async def get_nearby_profiles(data: NearbyProfilesRequest):
    db_manager = await get_db_manager()
    if not verify_request(data.token, data.profile_id):
        raise HTTPException(status_code=400, detail="Invalid id or token")

    location = await db_manager.get_location_by_id(data.profile_id)
    lat, lon = location.split(", ")

    uids = search_nearby_people(float(lat), float(lon), data.search_radius)
    return {"uids": uids}
