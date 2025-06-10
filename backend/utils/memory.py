import redis
import json
from os import getenv

r = redis.Redis(
    host=getenv("HOST"),
    port=getenv("PORT"),
    password=getenv("PASSWORD"),
    ssl=False
)


def getHistory(user_id):
    messages = r.lrange(f"chat:{user_id}", 0, -1)
    return [json.loads(m.decode()) for m in messages]

def addHistory(user_id, role, message):
    r.rpush(f"chat:{user_id}", json.dumps({"role": role, "content": message}))

def clearHistory(user_id):
    r.delete(f"chat:{user_id}")