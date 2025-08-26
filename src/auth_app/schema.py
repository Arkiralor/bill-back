from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class RegisterUserSchema(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(..., min_length=6, max_length=68)

class LoginUserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6, max_length=68)

class TokenSchema(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(default="bearer")

class LogoutSchema(BaseModel):
    refresh_token: str = Field(...)
    access_token: str = Field(...)

class ShowUserSchema(BaseModel):
    id: str = Field(...,)
    email: EmailStr = Field(...)
    username: str = Field(...)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(...)

class LogoutSchema(BaseModel):
    refresh_token: str = Field(...)
    access_token: str = Field(...)



