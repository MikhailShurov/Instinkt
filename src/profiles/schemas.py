from pydantic import BaseModel, validator


class GetProfileByID(BaseModel):
    token: str
    id: int


class Profile(BaseModel):
    email: str
    name: str
    age: int
    description: str
    hobbies: str
    preferences: str
    location: str
    contacts: str


class NewProfileInfo(BaseModel):
    name: str
    age: int
    description: str
    hobbies: str
    preferences: str
    location: str
    contacts: str


class ChangeProfileInfo(BaseModel):
    token: str
    new_info: NewProfileInfo
