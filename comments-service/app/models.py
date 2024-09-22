from sqlalchemy import Column, Integer, Text
from .database import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, index=True) 
    user_id = Column(Integer, index=True)
    content = Column(Text, nullable=False)

