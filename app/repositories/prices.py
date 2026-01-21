from datetime import datetime
from sqlalchemy import select, insert, func, and_
from app.schemas.prices import PriceCreate, PriceResponse, PriceListResponse
from app.models.price import Price
from app.repositories.base import BaseRepository


class PricesRepository(BaseRepository):
    model = Price

    async def add(self, data: PriceCreate) -> PriceResponse:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all_with_filters(
        self,
        ticker: str,
        limit: int = 100,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> PriceListResponse:
        conditions = [self.model.ticker == ticker]

        if date_from is not None:
            unix_from = int(date_from.timestamp())
            conditions.append(self.model.created_at >= unix_from)

        if date_to is not None:
            unix_to = int(date_to.timestamp())
            conditions.append(self.model.created_at <= unix_to)

        where_clause = and_(*conditions)

        query = (
            select(self.model)
            .where(where_clause)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        prices = result.scalars().all()

        count_query = select(func.count()).select_from(self.model).where(where_clause)
        count_result = await self.session.execute(count_query)
        total: int = count_result.scalar_one()

        return PriceListResponse(data=list(prices), total=total)

    async def get_latest(self, ticker: str) -> PriceResponse | None:
        query = (
            select(self.model)
            .where(self.model.ticker == ticker)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
