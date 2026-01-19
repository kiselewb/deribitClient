from datetime import datetime
from pydantic import BaseModel


class PriceAdd(BaseModel):
    ticker: str
    price: float


class Price(PriceAdd):
    id: int
    created_at: datetime
