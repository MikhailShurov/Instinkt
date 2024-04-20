from pydantic import BaseModel


class Like(BaseModel):
    initiator_id: int
    initiator_token: str
    profile_to_like_id: int


class GetLikes(BaseModel):
    initiator_id: int
    initiator_token: str
