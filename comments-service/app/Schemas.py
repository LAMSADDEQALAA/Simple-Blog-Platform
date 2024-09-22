from pydantic import BaseModel, ConfigDict

class CommentBase(BaseModel):
    content: str
    user_id: int
    post_id: int

class CommentUpdate(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

