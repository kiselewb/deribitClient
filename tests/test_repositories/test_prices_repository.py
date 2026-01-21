import pytest
from decimal import Decimal
from app.repositories.prices import PricesRepository
from app.schemas.prices import PriceCreate


class TestPricesRepositoryAdd:
    @pytest.mark.asyncio
    async def test_add_price(self, db_session, clear_db):
        repo = PricesRepository(db_session)

        price_data = PriceCreate(ticker="BTC_USD", price=Decimal("50000.00"))
        result = await repo.add(price_data)
        await db_session.commit()

        assert result.id is not None
        assert result.ticker == "BTC_USD"
        assert result.price == Decimal("50000.00")
        assert result.created_at is not None
        assert isinstance(result.created_at, int)

    @pytest.mark.asyncio
    async def test_add_multiple_prices(self, db_session):
        repo = PricesRepository(db_session)

        btc_data = PriceCreate(ticker="BTC_USD", price=Decimal("52000.00"))
        eth_data = PriceCreate(ticker="ETH_USD", price=Decimal("3000.00"))

        btc_result = await repo.add(btc_data)
        eth_result = await repo.add(eth_data)
        await db_session.commit()

        assert btc_result.id != eth_result.id
        assert btc_result.ticker == "BTC_USD"
        assert eth_result.ticker == "ETH_USD"


class TestPricesRepositoryGetLatest:
    @pytest.mark.asyncio
    async def test_get_latest_price(self, db_session):
        repo = PricesRepository(db_session)

        result = await repo.get_latest("BTC_USD")

        assert result is not None
        assert result.ticker == "BTC_USD"

        assert result.price == Decimal("52000.00")

    @pytest.mark.asyncio
    async def test_get_latest_returns_newest(self, db_session):
        repo = PricesRepository(db_session)

        old_price = PriceCreate(ticker="BTC_USD", price=Decimal("40000.00"))
        new_price = PriceCreate(ticker="BTC_USD", price=Decimal("60000.00"))

        await repo.add(old_price)
        await db_session.commit()

        import asyncio

        await asyncio.sleep(0.1)

        await repo.add(new_price)
        await db_session.commit()

        result = await repo.get_latest("BTC_USD")

        assert result.price == Decimal("60000.00")


class TestPricesRepositoryGetAllWithFilters:
    @pytest.mark.asyncio
    async def test_get_all_basic(self, db_session):
        repo = PricesRepository(db_session)

        result = await repo.get_all_with_filters(ticker="BTC_USD")

        assert result.total == 4
        assert len(result.data) == 4

    @pytest.mark.asyncio
    async def test_get_all_with_limit(self, db_session):
        repo = PricesRepository(db_session)

        result = await repo.get_all_with_filters(ticker="BTC_USD", limit=2)

        assert result.total == 4
        assert len(result.data) == 2

    @pytest.mark.asyncio
    async def test_get_all_with_offset(self, db_session):
        repo = PricesRepository(db_session)

        result = await repo.get_all_with_filters(ticker="BTC_USD", offset=2)

        assert result.total == 4
        assert len(result.data) == 2

    @pytest.mark.asyncio
    async def test_get_all_with_limit_and_offset(self, db_session):
        repo = PricesRepository(db_session)

        result = await repo.get_all_with_filters(ticker="BTC_USD", limit=1, offset=1)

        assert result.total == 4
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_get_all_filters_by_ticker(self, db_session):
        repo = PricesRepository(db_session)

        btc_result = await repo.get_all_with_filters(ticker="BTC_USD")
        eth_result = await repo.get_all_with_filters(ticker="ETH_USD")

        assert btc_result.total == 4
        assert eth_result.total == 1

        for price in btc_result.data:
            assert price.ticker == "BTC_USD"

        for price in eth_result.data:
            assert price.ticker == "ETH_USD"

    @pytest.mark.asyncio
    async def test_get_all_empty_result(self, db_session, clear_db):
        repo = PricesRepository(db_session)

        result = await repo.get_all_with_filters(ticker="BTC_USD")

        assert result.total == 0
        assert len(result.data) == 0
