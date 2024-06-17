import sys
import os
import pytest
import asyncio


from typing import Generator
from datetime import datetime

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, async_scoped_session, AsyncEngine
)

from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# service imports

from services.web.app.main import app
from services.db.app.database import Base, get_async_session
from domain.entities.meme.models.meme_model import Meme

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="module")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(init_db):
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_async_session] = lambda: TestingSessionLocal()
    with TestClient(app) as c:
        yield c