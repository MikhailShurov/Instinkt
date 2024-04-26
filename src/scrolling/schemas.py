from pydantic import BaseModel


class NearbyProfilesRequest(BaseModel):
    profile_id: int
    token: str
    search_radius: int
