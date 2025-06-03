from fastapi import FastAPI
from limiter.middleware import RateLimiterMiddleware
from limiter.rules_sync import RuleSync
import redis.asyncio as redis

app = FastAPI()

redis_client = redis.Redis(host="localhost", port=6379, db=0)
rule_sync = RuleSync(redis_client)

@app.on_event("startup")
async def startup_event():
    await rule_sync.start()

app.add_middleware(
    RateLimiterMiddleware,
    redis_client=redis_client,
    rule_sync=rule_sync
)

@app.get("/")
async def root():
    return {"message": "Hello from distributed rate limiter"}
