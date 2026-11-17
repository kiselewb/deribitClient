from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, Field, field_serializer
from decimal import Decimal


class PriceCreate(BaseModel):
    ticker: str
    price: Decimal = Field(json_schema_extra={"example": "45230.50"})

    @field_serializer("price")
    def serialize_price(self, price: Decimal) -> str:
        return f"{price:.2f}"


class PriceResponse(PriceCreate):
    id: int
    created_at: datetime

    @field_validator("created_at", mode="before")
    @classmethod
    def convert_unix_to_datetime(cls, v):
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v

    model_config = {"from_attributes": True}


class PriceListResponse(BaseModel):
    data: list[PriceResponse]
    total: int
