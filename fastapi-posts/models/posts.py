from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True
