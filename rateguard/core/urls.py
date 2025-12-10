from django.urls import path
from .views import ping, redis_test

urlpatterns = [
    path("ping/", ping),
    path("redis-test/", redis_test),
]
