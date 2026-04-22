import redis
import os

# connect to Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def get_cache(key: str):
    return redis_client.get(key)

def set_cache(key: str, value: str):
    redis_client.set(key, value, ex=300)  # expires in 5 min