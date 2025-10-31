from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


ASYNC_DATABASE_URL = "sqlite+aiosqlite:///Database/data.db" # Будет работать с ботом
SYNC_DATABASE_URL = "sqlite:///Database/data.db" # Будет работать с миграциями

ASYNC_ENGINE = create_async_engine(ASYNC_DATABASE_URL, echo=True)
SYNC_ENGINE = create_engine(SYNC_DATABASE_URL, echo=True)

async_session = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=True)
sync_session = sessionmaker(SYNC_ENGINE, expire_on_commit=True)

Base = declarative_base()