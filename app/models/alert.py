from decimal import Decimal
from datetime import datetime

from sqlalchemy import String, Numeric, Boolean, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    coin_symbol: Mapped[str] = mapped_column(String, index=True)
    # Target price stored as Decimal for financial precision
    target_price: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    # Timestamp when the alert was created
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # Optional: mark if the alert has been triggered
    triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    # Composite index for fast queries by coin + triggered status
    __table_args__ = (
        Index("ix_alerts_coin_triggered", "coin_symbol", "triggered"),
    )
