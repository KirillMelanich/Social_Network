from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, AnalyticsViewSet, UserActivityViewSet

routers = DefaultRouter()
routers.register("posts", PostViewSet, basename="posts")
routers.register("activity", UserActivityViewSet, basename="activity")
routers.register("analytics", AnalyticsViewSet, basename="analytics")

urlpatterns = [
    path("", include(routers.urls)),
]

app_name = "tweetogram"
