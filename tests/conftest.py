from decimal import Decimal
from typing import AsyncGenerator, Any
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.base import Base
from app.database.db_manager import DBManager
from app.api.dependencies import get_db
from app.database.database import async_test_session_maker, test_engine
from app.schemas.prices import PriceCreate


async def get_db_test():
    async with DBManager(session_factory=async_test_session_maker) as db:
        yield db


app.dependency_overrides[get_db] = get_db_test


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_test_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_test():
        yield db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def ac(setup_database) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        transport=ASGITransport(
            app=app,
            raise_app_exceptions=True,
        ),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def sample_prices(db):
    prices = [
        PriceCreate(ticker="BTC_USD", price=Decimal("50000.00")),
        PriceCreate(ticker="BTC_USD", price=Decimal("51000.00")),
        PriceCreate(ticker="BTC_USD", price=Decimal("52000.00")),
        PriceCreate(ticker="ETH_USD", price=Decimal("3000.00")),
        PriceCreate(ticker="ETH_USD", price=Decimal("3100.00")),
    ]

    for price in prices:
        await db.prices.add(price)
    await db.commit()

    return prices


@pytest_asyncio.fixture
async def clear_db(db):
    await db.prices.delete_all()
    await db.commit()
