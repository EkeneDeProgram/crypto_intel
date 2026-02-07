from decimal import Decimal
from datetime import datetime

from sqlalchemy import String, Numeric, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class MiningCoin(Base):
    __tablename__ = "mining_coins"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String, index=True)

    # Hash rate with high precision (Decimal) for accurate calculations
    hash_rate: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    # Power consumption with high precision (Decimal)
    power_consumption: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    # Timestamp when the record was created
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # Timestamp when the record was last updated
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Composite index for fast queries by symbol and hash_rate
    __table_args__ = (
        Index("ix_mining_coins_symbol_hash", "symbol", "hash_rate"),
    )
