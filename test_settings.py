# test_db.py
# from sqlalchemy import create_engine

# DATABASE_URL = "postgresql://postgres:sohelpmegod@localhost:5432/crypto_intel"

# engine = create_engine(DATABASE_URL)

# try:
#     with engine.connect() as conn:
#         print("✅ PostgreSQL connected successfully")
# except Exception as e:
#     print("❌ PostgreSQL connection failed:", e)







# test_redis.py
# import redis

# REDIS_URL = "redis://localhost:6379/0"

# r = redis.from_url(REDIS_URL)

# try:
#     r.set("health_check", "ok")
#     print("✅ Redis connected:", r.get("health_check").decode())
# except Exception as e:
#     print("❌ Redis connection failed:", e)




# test_coingecko.py
# import requests

# COINGECKO_API = "https://api.coingecko.com/api/v3"

# response = requests.get(f"{COINGECKO_API}/ping")
# print("Status:", response.status_code)
# print("Response:", response.json())
