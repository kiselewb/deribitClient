from datetime import datetime

from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.prices import PriceCreate
from app.services.prices import PricesService

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("")
async def get_prices(
    db: DBDep,
    ticker: str,
    limit: int = 100,
    offset: int = 0,
    date_from: datetime | None = None,
    date_to: datetime | None = None
):
    return await PricesService(db).get_all(ticker, limit, offset, date_from, date_to)

@router.get("/latest")
async def get_latest_price(
    db: DBDep,
    ticker: str
):
    return await PricesService(db).get_latest(ticker)

