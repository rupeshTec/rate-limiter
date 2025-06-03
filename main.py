# main.py

from fastapi import FastAPI
import redis.asyncio as redis
from limiter.middleware import RateLimiterMiddleware

app = FastAPI()

redis_client = redis.Redis(host="localhost", port=6379, db=0)

app.add_middleware(RateLimiterMiddleware, redis_client=redis_client)

@app.get("/")
async def root():
    return {"message": "Token bucket rate limiter working!"}
