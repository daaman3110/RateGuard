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
    ip = request.META.get("REMOTE_ADDR", "unknown")
    from .redis_service import get_counter

    return Response({"ip": ip, "count": get_counter(ip)})
