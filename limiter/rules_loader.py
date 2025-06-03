# limiter/rules_loader.py

import asyncio
import json
from redis.asyncio import Redis

async def load_rules_periodically(redis_client: Redis, interval: int = 10):
    while True:
        try:
            with open("rules.json", "r") as f:
                rules = json.load(f)
                await redis_client.set("rate_limit_rules", json.dumps(rules))
                print("✅ Rules loaded to Redis")
        except Exception as e:
            print(f"❌ Failed to load rules: {e}")
        await asyncio.sleep(interval)
