from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RequestLogSerializer
from .models import RequestLog
from .redis_service import increment_counter


# Create your views here.
@api_view(["GET"])
def ping(request):
    logs = RequestLog.objects.all().order_by("-timestamp")
    serializer = RequestLogSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def redis_test(request):
    # Get Client IP
    ip = request.META.get("REMOTE_ADDR", "unknown")

    # 1) Count requests per IP
    count = increment_counter(ip)

    # 2) Set the rate limit
    LIMIT = 5
    WINDOW = 60

    # 3) Apply limit rule
    if count > LIMIT:
        return Response(
            {
                "error": "Rate Limit Exceeded",
                "ip": ip,
                "count": count,
                "limit": LIMIT,
                "window": WINDOW,
            },
            status=429,
        )

    # 4) Allowed Request
    return Response({"message": "OK", "ip": ip, "count": count})
