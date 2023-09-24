from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from sqlalchemy import NullPool





if settings.MODE == 'TEST':
    DATABASE_URL = settings.test_DATABASE_URL
    PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    PARAMS = {}


engine = create_async_engine(DATABASE_URL, **PARAMS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



class Base(DeclarativeBase):
    pass
