from pydantic import BaseModel


class GetProfileByEmail(BaseModel):
    token: str
    email: str


class Profile(BaseModel):
    email: str
    name: str
    age: int
    description: str
    hobbies: str
    preferences: str
    location: str
    contacts: str


class ChangeProfileInfo(BaseModel):
    token: str
    email: str
    new_info: Profile
