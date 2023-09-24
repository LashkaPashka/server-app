from app.database import async_session_maker

from sqlalchemy import select, insert, text



class BaseDAO:
    model = None

    @classmethod
    async def get_db_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=user_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()


    @classmethod
    async def get_db_one_or_null(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()


    @classmethod
    async def get_db_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()


    @classmethod
    async def get_db(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add_users(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()



