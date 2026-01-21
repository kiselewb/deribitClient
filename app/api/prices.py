from datetime import datetime
from enum import Enum
from fastapi import APIRouter, Query, HTTPException
from starlette import status

from app.api.dependencies import DBDep
from app.schemas.prices import PriceCreate, PriceListResponse, PriceResponse
from app.services.prices import PricesService


class Ticker(str, Enum):
    BTC_USD = "BTC_USD"
    ETH_USD = "ETH_USD"


router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("")
async def get_prices(
    db: DBDep,
    ticker: Ticker,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> PriceListResponse:
    try:
        return await PricesService(db).get_all(
            ticker.value, limit, offset, date_from, date_to
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch prices: {str(e)}",
        )


@router.get("/latest")
async def get_latest_price(db: DBDep, ticker: Ticker) -> PriceResponse:
    try:
        price = await PricesService(db).get_latest(ticker.value)

        if not price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No prices found for ticker {ticker.value}",
            )

        return price

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch latest price: {str(e)}",
        )


@router.post("")
async def create_price(db: DBDep, data: PriceCreate) -> PriceResponse:
    try:
        return await PricesService(db).add_price(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create price: {str(e)}",
        )
