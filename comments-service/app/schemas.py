from pydantic import BaseModel, constr, conint, validator, ConfigDict


class CommentBase(BaseModel):
    content: constr(min_length=1, max_length=500)
    user_id: conint(gt=0)
    post_id: conint(gt=0)  

class CommentUpdate(BaseModel):
    content: constr(min_length=1, max_length=500)

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id:int

    @validator('content')
    def validate_content(cls, value):
        if not value.strip():
            raise ValueError('Content cannot be empty or whitespace')
        return value
