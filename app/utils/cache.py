# app/utils/cache.py
import redis
import json
from app.core.config import settings

# Create Redis client
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Get cached value from Redis
def get_cache(key: str):
    value = redis_client.get(key)
    return json.loads(value) if value else None  # Convert JSON string to Python object

# Set value in Redis with expiration
def set_cache(key: str, value, expire_seconds: int = 300):
    redis_client.set(key, json.dumps(value), ex=expire_seconds)  # Store Python object as JSON
