import redis
import os

# connect to Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def get_history(session_id: str):
    return redis_client.lrange(session_id, 0, -1)

def add_history(session_id: str, message: str):
    redis_client.rpush(session_id, message)
    redis_client.expire(session_id, 600)
    
def get_cache(key: str):
    return redis_client.get(key)

def set_cache(key: str, value: str):
    redis_client.set(key, value, ex=300)  # expires in 5 min