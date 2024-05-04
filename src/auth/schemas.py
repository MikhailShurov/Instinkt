from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    password: str


class UpdatePrimeStatus(BaseModel):
    token: str
    prime: bool


class UserModel(BaseModel):
    token: str
