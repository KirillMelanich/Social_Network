from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PostViewSet


routers = DefaultRouter()
routers.register("posts", PostViewSet)

urlpatterns = [
    path("", include(routers.urls)),
]

app_name = "tweetogram"
