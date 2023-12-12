from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, AnalyticsViewSet, UserActivityViewSet

routers = DefaultRouter()
routers.register("posts", PostViewSet, basename="posts")
routers.register("activity", UserActivityViewSet, basename="activity")

urlpatterns = [
    path("", include(routers.urls)),
    path(
        "analytics/", AnalyticsViewSet.as_view({"get": "list"}), name="analytics-list"
    ),
]

app_name = "tweetogram"


# http://127.0.0.1:8000/api/tweetogram/analytics/?date_from=2023-12-11&date_to=2023-12-13
