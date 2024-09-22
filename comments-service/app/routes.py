from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .dependencies import get_db
from . import models, schemas
from typing import List
from .cache import cache
import logging

logger = logging.getLogger()
comment_router = APIRouter(prefix="/api")

@comment_router.get("/comments", response_model=List[schemas.Comment])
async def read_comments(db: AsyncSession = Depends(get_db)):
    comments = await db.scalars(select(models.Comment))
    return [schemas.Comment.model_validate(comment) for comment in comments]


@comment_router.get("/posts/{post_id}/comments", response_model=List[schemas.Comment])
async def read_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    cache_key = f"comments_post_{post_id}"
    cached_comments = await cache.get(cache_key)

    if cached_comments is not None:
        logger.info("returned from cache")
        return cached_comments

    comments = await db.scalars(select(models.Comment).filter(models.Comment.post_id == post_id))
    comment_list = [schemas.Comment.model_validate(comment).model_dump() for comment in comments]

    await cache.set(cache_key, comment_list, ttl=60*15)
    logger.info("not returned from cache")
    return comment_list


@comment_router.post("/comments",status_code=status.HTTP_201_CREATED)
async def create_comment(comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db)) -> schemas.Comment:
    new_comment = models.Comment(**comment.model_dump())
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return schemas.Comment.model_validate(new_comment)


@comment_router.put("/comments/{comment_id}", response_model=schemas.Comment)
async def update_comment(comment_id: int, comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db)):
    existing_comment = await db.scalar(select(models.Comment).filter(models.Comment.id == comment_id))
    
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    for key, value in comment.model_dump().items():
        setattr(existing_comment, key, value)
    
    await db.commit()
    await db.refresh(existing_comment)
    return existing_comment

@comment_router.delete("/comments/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    existing_comment = await db.scalar(select(models.Comment).filter(models.Comment.id == comment_id))
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    await db.delete(existing_comment)
    await db.commit()
    return
