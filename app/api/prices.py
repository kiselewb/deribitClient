from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.prices import PriceAdd
from app.services.prices import PricesService

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("")
async def get_prices(db: DBDep):
    return await PricesService(db).get_prices()


@router.post("")
async def create_price(db: DBDep, price_data: PriceAdd = Body()):
    price = await PricesService(db).add_price(price_data)
    return {"status": "OK", "price": price}
