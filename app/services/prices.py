from datetime import datetime

from app.services.base import BaseService


class PricesService(BaseService):
    async def get_all(
            self,
            ticker: str,
            limit: int = 100,
            offset: int = 0,
            date_from: datetime | None = None,
            date_to: datetime | None = None
    ) -> tuple[list, int]:
        pass

    async def get_latest(self, ticker: str):
        pass
