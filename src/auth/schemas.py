from typing import Optional

from pydantic import EmailStr, BaseModel


class UserRegistration(BaseModel):
    email: str
    password: str