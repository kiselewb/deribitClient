from datetime import datetime

from app.schemas.prices import PriceResponse
from app.services.base import BaseService


class PricesService(BaseService):
    async def get_all(
        self,
        ticker: str,
        limit: int = 100,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> tuple[list[PriceResponse], int]:
        return await self.db.prices.get_all_with_filters(
            ticker, limit, offset, date_from, date_to
        )

    async def get_latest(self, ticker: str) -> PriceResponse:
        return await self.db.prices.get_latest(ticker)
