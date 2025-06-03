# middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import time

# Configurable rate limit parameters
MAX_TOKENS = 10
REFILL_RATE = 1  # tokens per second

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client):
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        tokens_key = f"tokens:{client_ip}"
        timestamp_key = f"timestamp:{client_ip}"

        now = time.time()

        try:
            pipe = self.redis.pipeline()
            pipe.get(tokens_key)
            pipe.get(timestamp_key)
            tokens_str, last_refill_str = await pipe.execute()

            tokens = float(tokens_str) if tokens_str else MAX_TOKENS
            last_refill = float(last_refill_str) if last_refill_str else now

            # Refill tokens
            elapsed = now - last_refill
            new_tokens = min(MAX_TOKENS, tokens + elapsed * REFILL_RATE)

            if new_tokens >= 1:
                new_tokens -= 1
                pipe = self.redis.pipeline()
                pipe.set(tokens_key, new_tokens)
                pipe.set(timestamp_key, now)
                await pipe.execute()
            else:
                return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

        except Exception as e:
            print(f"Rate limiter error: {e}")
            # Fail open
            pass

        response = await call_next(request)
        return response
