import uuid

from asyncio import current_task
from typing import AsyncIterator

from sqlalchemy import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine, async_scoped_session, AsyncEngine
)


# internal module imports
from settings.settings import get_settings


settings = get_settings()


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.session = None

    def init_db(self):

        self.engine = create_async_engine(
            settings.DATABASE_URL, pool_size=100, max_overflow=0, pool_pre_ping=False
        )

        self.session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )

        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    async def close(self):

        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()


sessionmanager = DatabaseSessionManager()
sessionmanager.init_db()


async def get_async_session() -> AsyncIterator[AsyncSession]:
    a = sessionmanager
    session = sessionmanager.session()
    if session is None:
        raise Exception("DatabaseSessionManager is not initialized")
    try:
        yield session
    except Exception as ex:
        await session.close()
        print(ex)
    finally:
        await session.close()


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        name = cls.__name__.lower()
        if 'model' in name:
            return name.replace('model', '')

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )

