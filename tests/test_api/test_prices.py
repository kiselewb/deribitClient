import pytest


class TestGetPrices:
    @pytest.mark.asyncio
    async def test_get_prices_success(self, ac, sample_prices):
        response = await ac.get("/prices", params={"ticker": "BTC_USD"})

        assert response.status_code == 200
        data = response.json()

        assert "data" in data
        assert "total" in data
        assert data["total"] == 3
        assert len(data["data"]) == 3

        first_price = data["data"][0]
        assert "id" in first_price
        assert "ticker" in first_price
        assert "price" in first_price
        assert "created_at" in first_price
        assert first_price["ticker"] == "BTC_USD"

    @pytest.mark.asyncio
    async def test_get_prices_with_limit(self, ac):
        response = await ac.get("/prices?ticker=BTC_USD&limit=2")

        assert response.status_code == 200
        data = response.json()

        assert len(data["data"]) == 2
        assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_get_prices_with_offset(self, ac):
        response = await ac.get("/prices?ticker=BTC_USD&offset=2")

        assert response.status_code == 200
        data = response.json()

        assert len(data["data"]) == 1
        assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_get_prices_invalid_ticker(self, ac):
        response = await ac.get("/prices?ticker=INVALID_TICKER")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_get_prices_limit_validation(self, ac):
        response = await ac.get("/prices?ticker=BTC_USD&limit=2000")
        assert response.status_code == 422

        response = await ac.get("/prices?ticker=BTC_USD&limit=0")
        assert response.status_code == 422


class TestGetLatestPrice:
    @pytest.mark.asyncio
    async def test_get_latest_success(self, ac):
        response = await ac.get("/prices/latest?ticker=BTC_USD")

        assert response.status_code == 200
        data = response.json()

        assert data["ticker"] == "BTC_USD"
        assert "price" in data
        assert "created_at" in data
        assert data["price"] == "52000.00"

    @pytest.mark.asyncio
    async def test_get_latest_eth(self, ac):
        response = await ac.get("/prices/latest?ticker=ETH_USD")

        assert response.status_code == 200
        data = response.json()

        assert data["ticker"] == "ETH_USD"
        assert data["price"] == "3100.00"

    @pytest.mark.asyncio
    async def test_get_latest_invalid_ticker(self, ac):
        response = await ac.get("/prices/latest?ticker=INVALID")

        assert response.status_code == 422


class TestCreatePrice:
    @pytest.mark.asyncio
    async def test_create_price_success(self, ac):
        payload = {"ticker": "BTC_USD", "price": "45000.50"}

        response = await ac.post("/prices", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["ticker"] == "BTC_USD"
        assert data["price"] == "45000.50"
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_price_validation(self, ac):
        response = await ac.post("/prices", json={})
        assert response.status_code == 422

        response = await ac.post(
            "/prices", json={"ticker": "BTC_USD", "price": "invalid"}
        )
        assert response.status_code == 422
