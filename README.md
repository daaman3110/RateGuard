# RateGuard: Django Rate Limiter with Redis + Middleware + Postgres Logging

A production-style Django project implementing API rate limiting using Redis and custom middleware. Every incoming request is:

1. Processed through middleware
2. Rate-checked via Redis
3. Allowed or blocked (429)
4. Logged into Postgres for analytics

This project demonstrates a real-world backend pattern used in high-scale systems.

---

## Features

### 1. Custom Rate Limiting Middleware
* Limits requests based on client IP
* Tracks counts inside Redis
* Automatically blocks requests with HTTP 429 Too Many Requests
* Threshold and TTL are configurable

### 2. Redis Integration
Used as a high-speed in-memory counter for:
* IP hit tracking
* Expiring counters (e.g., 60 seconds)
* Efficient rate limiting

### 3. Postgres Logging
Every request (allowed or blocked) is persisted in DB with:
* IP Address
* Path
* HTTP method
* Response status
* Timestamp

Useful for monitoring, analytics, and debugging.

### 4. Simple API Endpoints
* `/api/ping/` — Simple test endpoint and returns logs from Postgres DB
* `/api/redis-test/` — Additional sample endpoint to test rate limits

---

## Architecture Overview

```
Client Request
        ↓
Django Middleware
        ↓
  Redis Check
   ├── Counter < limit → Allow & log
   └── Counter >= limit → Block (429) & log
        ↓
  Django View (if allowed)
        ↓
   Response to Client
```

---

## Technologies Used

* Python 3.13.9
* Django 5+
* Redis
* PostgreSQL
* Docker 

---

## Installation & Setup

### 1️: Clone the repo

```bash
git clone https://github.com/yourusername/rate-limiter.git
cd rate-limiter
```

### 2️: Create virtual environment

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3: Start Redis

If using Docker:

```bash
docker run -d -p 6379:6379 redis
```

### 4: Run migrations

```bash
python manage.py migrate
```

### 5: Start server

```bash
python manage.py runserver
```

---

## Testing the Rate Limiter

Hit the same endpoint multiple times:

```bash
curl http://127.0.0.1:8000/api/ping/
```

After the rate limit is exceeded, you'll receive:

```
HTTP 429 Too Many Requests
```

And logs will appear in Postgres:

<img width="1033" height="577" alt="image" src="https://github.com/user-attachments/assets/bbe8c55f-ba04-4e13-939b-65059d0aa901" />


---

## Middleware Behavior Summary

1. Extract client IP
2. Generate Redis key for IP
3. Increment request count
4. Compare with threshold
5. Either:
   * Allow request and pass to view
   * Block with 429
6. Log request into Postgres

---

## Configurable Settings

Inside middleware:

```python
RATE_LIMIT = 5          # max requests
WINDOW_SECONDS = 10     # time window
```

Adjust these according to your use case.

---

