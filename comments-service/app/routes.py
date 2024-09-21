from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .dependencies import get_db
from typing import List

comment_router = APIRouter()

@comment_router.get("posts/{post_id}/comments/", response_model=List[schemas.Comment])
def read_comments(post_id: int,db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments