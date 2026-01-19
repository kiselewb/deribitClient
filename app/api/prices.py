from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.prices import PriceCreate
from app.services.prices import PricesService

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("")
async def get_prices(db: DBDep):
    return await PricesService(db).get_all()

