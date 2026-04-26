# Service → Queue → Worker → DB

import redis
import json

# connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

QUEUE_NAME = "log_queue"

def push_log(log):
    print("👉 [QUEUE] Adding to Redis:", log)
    r.lpush(QUEUE_NAME, json.dumps(log))

def pop_log():
    data = r.rpop(QUEUE_NAME)
    if data:
        log = json.loads(data)
        print("👉 [QUEUE] Popped from Redis:", log)
        return log
    return None