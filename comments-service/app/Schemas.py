from pydantic import BaseModel
from typing import List, Optional

class CommentBase(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
