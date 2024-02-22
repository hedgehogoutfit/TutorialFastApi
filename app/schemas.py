from pydantic import BaseModel
from pydantic.types import conint
from typing import Optional
from datetime import datetime


class PostStr(BaseModel):
    title: str
    content: str
    published: bool = True  # default to true


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostRes(PostStr):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: PostRes
    votes_count: int


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

