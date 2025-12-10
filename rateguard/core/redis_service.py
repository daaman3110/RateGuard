import redis

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def generate_key(ip: str) -> str:
    return f"ratelimit:{ip}"


def get_counter(ip: str):
    key = generate_key(ip)
    value = r.get(key)
    return int(value) if value else 0


def increment_counter(ip: str):
    key = generate_key(ip)

    current = r.get(key)

    if current is None:
        # First Request -> Set with expiry
        r.set(key, 1, ex=60)
        return 1
    else:
        # Increment existing counter
        return r.incr(key)
