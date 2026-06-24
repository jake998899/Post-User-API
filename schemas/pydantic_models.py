from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Literal

class UserReq(BaseModel):
    username: str = Field(..., min_length=3, max_length=250, pattern=r'^[a-zA-Z\d\!\$\%]+$', examples=['Ali$Pro123'])
    email: EmailStr = Field(..., min_length=1, max_length=250, examples=['example@gmail.com'])
    role: Literal['user', 'admin'] = Field(...)
    password: str = Field(...)

    model_config = ConfigDict(str_strip_whitespace=True, str_to_lower=True)

class UserReqRes(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordEmail(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=250, examples=['example@gmail.com'])

class ResetPasswordReq(BaseModel):
    password: str = Field(..., min_length=6, examples=['test123'])