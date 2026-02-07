# app/services/market_service.py
from typing import List, Dict
from decimal import Decimal
from datetime import datetime

from app.utils.http import get_json
from app.utils.cache import get_cache, set_cache
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.coin import Coin

CACHE_KEY = "market_data"


def get_market_data(coin_ids: List[str], use_cache: bool = True) -> Dict[str, Decimal]:
    """
    Fetch current prices from CoinGecko by coin IDs, update DB,
    cache results in Redis. Uses Decimal for precision and stores correct symbols.

    Args:
        coin_ids (List[str]): List of CoinGecko coin IDs
        use_cache (bool): If True, try Redis cache first

    Returns:
        Dict[str, Decimal]: Mapping of coin_id -> current price in USD
    """
    # Try Redis cache first
    if use_cache:
        cached = get_cache(CACHE_KEY)
        if cached:
            return {k: Decimal(v) for k, v in cached.items()}

    # Fetch CoinGecko data
    data = get_json(
        f"{settings.COINGECKO_API}/simple/price",
        params={"ids": ",".join(coin_ids), "vs_currencies": "usd", "include_symbol": "true"}
    )

    prices: Dict[str, Decimal] = {}

    # Safe DB session
    with SessionLocal() as db:
        for coin_id in coin_ids:
            if coin_id not in data:
                continue

            price = Decimal(str(data[coin_id]["usd"]))
            prices[coin_id] = price

            # Try to get CoinGecko symbol from DB API response if available
            cg_symbol = data[coin_id].get("symbol", coin_id[:5].upper())

            # Update DB
            coin = db.query(Coin).filter(Coin.coin_id == coin_id).first()
            if coin:
                coin.price = price
                coin.symbol = cg_symbol  # ensure correct symbol
                coin.last_updated = datetime.utcnow()
            else:
                # Add new coin with correct symbol
                coin = Coin(
                    coin_id=coin_id,
                    symbol=cg_symbol,
                    name=coin_id.capitalize(),
                    price=price,
                    market_cap=Decimal("0.0"),
                    first_seen=datetime.utcnow(),
                    last_updated=datetime.utcnow(),
                    is_new=True
                )
                db.add(coin)

        db.commit()

    # Cache in Redis
    if use_cache:
        set_cache(CACHE_KEY, {k: str(v) for k, v in prices.items()}, expire_seconds=300)

    return prices
