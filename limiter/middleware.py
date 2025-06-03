# middleware.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json
import time

QUEUE_NAME = "request_queue"

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client, rule_sync):
        super().__init__(app)
        self.redis_client = redis_client
        self.rule_sync = rule_sync  # 👈 store RuleSync instance

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # 👇 access rules safely
        rules = self.rule_sync.rules or {}
        rule = rules.get(client_ip) or rules.get("default")

        if not rule or "rate" not in rule or "window" not in rule:
            rule = {"rate": 3, "window": 60}

        rate_limit = rule["rate"]
        window_size = rule["window"]

        try:
            count = await self.redis_client.incr(key)
            if count == 1:
                await self.redis_client.expire(key, window_size)

            if count > rate_limit:
                request_data = {
                    "ip": client_ip,
                    "path": request.url.path,
                    "method": request.method,
                    "timestamp": int(time.time())
                }

                await self.redis_client.lpush(QUEUE_NAME, json.dumps(request_data))
                print(f"⚠️ Request queued for {client_ip}")

                return JSONResponse(
                    status_code=202,
                    content={"message": "Too many requests. Your request has been queued."}
                )

        except Exception as e:
            print(f"Rate limiter error: {e}")

        return await call_next(request)
