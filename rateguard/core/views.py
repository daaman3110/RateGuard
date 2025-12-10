from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RequestLogSerializer
from .models import RequestLog


# Create your views here.
@api_view(["GET"])
def ping(request):
    logs = RequestLog.objects.all().order_by('-timestamp')
    serializer = RequestLogSerializer(logs, many=True)
    return Response(serializer.data)
