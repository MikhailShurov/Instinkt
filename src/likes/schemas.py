from pydantic import BaseModel


class Like(BaseModel):
    token: str
    profile_to_like_id: int
