from sqlalchemy import select, insert

from app.schemas.prices import PriceAdd


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def add(self, data: PriceAdd):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
