from app.models.price import Price
from app.repositories.base import BaseRepository


class PricesRepository(BaseRepository):
    model = Price
