# ⚡ Rate Limiter with Redis Queue and Distributed Rule Sync

A robust, extendable FastAPI-based rate limiter with Redis-backed queueing and dynamic, distributed rule syncing.  
Supports IP-based throttling and pushes excess requests to a Redis queue for later handling.

---

## 🚀 Features
- IP-based **rate limiting**
- **Request queueing** for throttled users
- **Distributed rule sync** using Redis
- Middleware-based implementation for easy plug-and-play
- Docker-based Redis setup
- Virtual environment setup for clean dependency isolation

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Redis](https://redis.io/) (via Docker)
- [aioredis](https://github.com/aio-libs/aioredis)
- [Uvicorn](https://www.uvicorn.org/) ASGI server
- JSON-based dynamic rule loading

---

## 🗂️ Project Structure

rate-limiter/
│
├── limiter/
│ ├── main.py # FastAPI app entry point
│ ├── middleware.py # Rate limiter middleware logic
│ ├── rules.json # Rate limiting rules per IP or default
│
├── worker/
│ └── queue_worker.py # Redis queue consumer (optional)
│
├── main.py
├── docker-compose.yml # Redis container setup
├── venv/ # Virtual environment (excluded in .gitignore)
├── requirements.txt
└── README.md


---

## 🧑‍💻 Setup Instructions

### 1. 📁 Clone the Repo
git clone https://github.com/your-username/rate-limiter.git
cd rate-limiter

2. 🐍 Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. 📦 Install Dependencies
pip install -r requirements.txt

5. 🐳 Start Redis with Docker
Make sure Docker is installed and running.

docker compose -f docker/docker-compose.yml up -d
This will start Redis at localhost:6379.

5. 🏁 Run the App
uvicorn app.main:app --reload
App will be live at: http://127.0.0.1:8000

🧪 How It Works
🔐 Rate Limiting
Based on the rules.json file, each IP has a defined rate and window.

If a client exceeds the limit, their request is not rejected — it’s queued in Redis instead.

📥 Queuing Logic
Queued requests are stored in Redis under the key request_queue.
{
  "ip": "127.0.0.1",
  "path": "/api/data",
  "method": "GET",
  "timestamp": 1717521740
}
⚙️ Rules Configuration
{
  "default": {
    "rate": 3,
    "window": 60
  },
  "192.168.0.100": {
    "rate": 10,
    "window": 30
  }
}
"rate" → max requests

"window" → per X seconds

Update rules.json anytime — Redis Pub/Sub will sync rules across all app instances automatically.

🛠 Optional: Start the Redis Queue Worker
If you want to process queued requests:

python worker/queue_worker.py
You can modify queue_worker.py to:

Retry requests
Log them to a DB
Notify admins, etc.

📌 Notes
Uses async Redis client for high performance.
You can scale across multiple servers, and the rules will sync via Redis pub/sub.

🧹 To Do
 Expose rule update API
 Admin dashboard for queued request monitoring
 Request reprocessing
 Persistent logging (e.g., MongoDB, Postgres)

🧑‍🎓 Author
Rupesh Kumar
