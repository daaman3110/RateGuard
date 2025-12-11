from django.http import JsonResponse
from .redis_service import increment_counter, get_counter
from .models import RequestLog

RATE_LIMIT = 5  # Allowed Requests per minute


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip = request.META.get("REMOTE_ADDR", "unknown")

        # Increment counter for the IP
        count = increment_counter(ip)

        # Check if limit exceeded -> Block + Log
        if count > RATE_LIMIT:
            RequestLog.objects.create(
                ip_address=ip, path=request.path, method=request.method, status=429
            )
            return JsonResponse(
                {"error": "Too many requests", "ip": ip, "count": count}, status=429
            )

        # If allowed -> get response from view
        response = self.get_response(request)

        # Log this request into Postgres
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            method=request.method,
            status=str(response.status_code),
        )

        return response
