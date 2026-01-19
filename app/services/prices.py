from app.schemas.prices import PriceAdd
from app.services.base import BaseService


class PricesService(BaseService):
    async def add_price(self, price_data: PriceAdd):
        price = await self.db.prices.add(price_data)
        await self.db.commit()
        return price

    async def get_prices(self):
        return await self.db.prices.get_all()
