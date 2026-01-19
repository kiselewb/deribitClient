from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal


class PriceCreate(BaseModel):
    ticker: str
    price: Decimal


class PriceResponse(PriceCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PriceListResponse(BaseModel):
    data: list[PriceResponse]
    total: int
    limit: int
    offset: int


class LatestPriceResponse(BaseModel):
    ticker: str
    price: Decimal
    created_at: datetime
