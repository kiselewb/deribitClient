from sqlalchemy import String, Numeric, Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from decimal import Decimal
from app.models.base import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    created_at: Mapped[int] = mapped_column(
        BigInteger,
        server_default=func.extract("epoch", func.now()).cast(BigInteger),
        nullable=False,
    )

    __table_args__ = (Index("ix_ticker_created_at", "ticker", "created_at"),)
