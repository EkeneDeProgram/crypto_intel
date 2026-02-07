# app/services/discovery_service.py
from typing import List, Dict
from decimal import Decimal
from datetime import datetime

from app.utils.http import get_json
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.coin import Coin
from app.utils.cache import get_cache, set_cache  # Redis cache

CACHE_KEY = "newest_coins"


def discover_new_coins(vs_currency: str = "usd", per_page: int = 10) -> List[Dict]:
    """
    Fetch newest coins from CoinGecko, update DB with first_seen and last_updated,
    cache in Redis, and mark truly new coins as is_new.

    Args:
        vs_currency (str): Currency to compare prices (default 'usd')
        per_page (int): Number of coins to return (default 10)

    Returns:
        List[Dict]: List of newest coins with coin_id, symbol, name, price, and market_cap
    """
    # Try Redis cache first
    cached = get_cache(CACHE_KEY)
    if cached:
        # Convert cached strings back to Decimal
        return [
            {
                **coin,
                "current_price": Decimal(coin["current_price"]),
                "market_cap": Decimal(coin["market_cap"])
            }
            for coin in cached
        ]

    # Fetch from CoinGecko
    url = f"{settings.COINGECKO_API}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_asc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False
    }
    data = get_json(url, params=params)
    newest_coins = []

    # Safe DB session
    with SessionLocal() as db:
        for coin_data in data:
            coin_id = coin_data["id"]
            symbol = coin_data["symbol"]
            name = coin_data["name"]
            price = Decimal(str(coin_data["current_price"]))
            market_cap = Decimal(str(coin_data["market_cap"]))

            # Check if coin exists
            existing_coin = db.query(Coin).filter(Coin.coin_id == coin_id).first()

            if not existing_coin:
                # Truly new coin
                coin = Coin(
                    coin_id=coin_id,
                    symbol=symbol,
                    name=name,
                    price=price,
                    market_cap=market_cap,
                    is_new=True,
                    first_seen=datetime.utcnow(),
                    last_updated=datetime.utcnow()
                )
                db.add(coin)
            else:
                # Update existing coin
                existing_coin.name = name
                existing_coin.symbol = symbol
                existing_coin.price = price
                existing_coin.market_cap = market_cap
                existing_coin.is_new = False
                existing_coin.last_updated = datetime.utcnow()

            # Prepare return data
            newest_coins.append({
                "coin_id": coin_id,
                "symbol": symbol,
                "name": name,
                "current_price": price,
                "market_cap": market_cap
            })

        db.commit()

    # Cache results in Redis (Decimal → str for JSON)
    cache_data = [
        {**coin, "current_price": str(coin["current_price"]), "market_cap": str(coin["market_cap"])}
        for coin in newest_coins
    ]
    set_cache(CACHE_KEY, cache_data, expire_seconds=300)

    return newest_coins
