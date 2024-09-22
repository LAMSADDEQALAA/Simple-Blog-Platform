from .database import factory
from sqlalchemy import exc

async def get_db():
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise