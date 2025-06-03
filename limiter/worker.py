# worker.py

import redis
import json
import time

r = redis.Redis(host="localhost", port=6379, db=0)

QUEUE_NAME = "request_queue"

print("📥 Worker started, waiting for jobs...")

while True:
    _, raw_data = r.brpop(QUEUE_NAME)
    request_data = json.loads(raw_data)

    print(f"✅ Processing queued request: {request_data}")
    # Simulate request handling
    time.sleep(1)
