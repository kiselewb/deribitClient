from app.models.prices import PricesOrm
from app.repositories.base import BaseRepository


class PricesRepository(BaseRepository):
    model = PricesOrm
