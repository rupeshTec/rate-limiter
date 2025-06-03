# rule_sync.py

import asyncio
import json

REDIS_RULE_KEY = "rate_limit_rules"
REDIS_PUBSUB_CHANNEL = "rules:update"

class RuleSync:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.rules = {}

    async def load_rules(self):
        rules_raw = await self.redis_client.get(REDIS_RULE_KEY)
        if rules_raw:
            self.rules = json.loads(rules_raw)
            print("✅ Rules loaded to memory")
        else:
            self.rules = {}
            print("⚠️ No rules found in Redis")

    async def watch_for_updates(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(REDIS_PUBSUB_CHANNEL)
        print("📡 Listening for rule updates...")

        async for message in pubsub.listen():
            if message["type"] == "message":
                print("🔁 Reloading rules from Redis...")
                await self.load_rules()

    async def start(self):
        await self.load_rules()
        asyncio.create_task(self.watch_for_updates())
