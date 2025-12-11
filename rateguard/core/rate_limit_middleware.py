from django.http import JsonResponse
from .redis_service import increment_counter, get_counter

RATE_LIMIT = 5  # Allowed Requests per minute


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip = request.META.get("REMOTE_ADDR", "unknown")

        # Increment counter for the IP
        count = increment_counter(ip)

        # Check if limit exceeded
        if count > RATE_LIMIT:
            return JsonResponse(
                {"error": "Too many requests", "ip": ip, "count": count}, status=429
            )

        # Continue to view
        return self.get_response(request)
