from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .dependencies import get_db
from . import models, schemas
from typing import List
from .cache import cache
import logging
from .middlewares import jwt_validation

logger = logging.getLogger()
comment_router = APIRouter(prefix="/api")


@comment_router.get("/posts/{post_id}/comments",  status_code=status.HTTP_200_OK)
async def read_comments(post_id: int,user: dict = Depends(jwt_validation) , db: AsyncSession = Depends(get_db)) -> List[schemas.Comment]:
    cache_key = f"comments_post_{post_id}"
    cached_comments = await cache.get(cache_key)

    if cached_comments is not None:
        logger.info("returned from cache")
        return cached_comments

    comments = await db.scalars(select(models.Comment).filter(models.Comment.post_id == post_id))
    comment_list = [schemas.Comment.model_validate(comment).model_dump() for comment in comments]

    logger.info("not returned from cache")
    return comment_list


@comment_router.post("/comments",status_code=status.HTTP_201_CREATED)
async def create_comment(comment: schemas.CommentCreate,user: dict = Depends(jwt_validation) , db: AsyncSession = Depends(get_db)) -> schemas.Comment:
    new_comment = models.Comment(**comment.model_dump())
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    await cache.delete(f"comments_post_{new_comment.post_id}")
    return schemas.Comment.model_validate(new_comment)


@comment_router.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(comment_id: int, comment: schemas.CommentUpdate,user: dict = Depends(jwt_validation) , db: AsyncSession = Depends(get_db)):
    existing_comment = await db.scalar(select(models.Comment).filter(models.Comment.id == comment_id))
    
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    for key, value in comment.model_dump().items():
        setattr(existing_comment, key, value)
    
    await db.commit()
    await db.refresh(existing_comment)
    await cache.delete(f"comments_post_{existing_comment.post_id}")
    return existing_comment

@comment_router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int,user: dict = Depends(jwt_validation) , db: AsyncSession = Depends(get_db)):
    existing_comment = await db.scalar(select(models.Comment).filter(models.Comment.id == comment_id))
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    await db.delete(existing_comment)
    await db.commit()
    await cache.delete(f"comments_post_{existing_comment.post_id}")
    return
