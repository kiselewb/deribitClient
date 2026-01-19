from datetime import datetime
from sqlalchemy import select, func, and_
from app.models.price import Price
from app.repositories.base import BaseRepository


class PricesRepository(BaseRepository):
    model = Price

    async def get_all_with_filters(
        self,
        ticker: str,
        limit: int = 100,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> tuple[list[Price], int]:
        conditions = [Price.ticker == ticker]

        if date_from is not None:
            conditions.append(Price.created_at >= date_from)

        if date_to is not None:
            conditions.append(Price.created_at <= date_to)

        where_clause = and_(*conditions)

        query = (
            select(Price)
            .where(where_clause)
            .order_by(Price.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        prices = result.scalars().all()

        count_query = select(func.count()).select_from(Price).where(where_clause)
        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()

        return list(prices), total

    async def get_latest(self, ticker: str) -> Price | None:
        query = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.created_at.desc())
            .limit(1)
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
