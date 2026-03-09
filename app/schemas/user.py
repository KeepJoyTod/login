from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

UsernameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=50)]


class UserRegisterRequest(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]
    phone: Annotated[str | None, Field(min_length=6, max_length=20)] = None


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


class UserLoginRequest(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    password: Annotated[str, StringConstraints(min_length=1)]


class CurrentUserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    phone: str | None = None
