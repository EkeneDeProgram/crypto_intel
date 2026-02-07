# app/models/coin.py
from decimal import Decimal
from datetime import datetime

from sqlalchemy import String, Boolean, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Coin(Base):
    __tablename__ = "coins"

    # Local primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # CoinGecko unique ID to avoid symbol vs ID confusion
    coin_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Human-readable symbol, e.g., BTC
    symbol: Mapped[str] = mapped_column(String, index=True)

    name: Mapped[str] = mapped_column(String)

    # High-precision financial data
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    market_cap: Mapped[Decimal] = mapped_column(Numeric(18, 2))

    # Track if coin is new
    is_new: Mapped[bool] = mapped_column(Boolean, default=True)

    # Track when first discovered and last updated
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
