from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Post, Like, Dislike, Analytics, UserActivity
from .serializers import PostSerializer, AnalyticsSerializer, UserActivitySerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        Like.objects.create(user=user, post=post)
        post.likes += 1
        post.save()

        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        Dislike.objects.create(user=user, post=post)
        post.dislikes += 1
        post.save()

        return Response(
            {"detail": "Post disliked successfully."}, status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        # Check if the requesting user is the creator of the post
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post.")

        # Delete the post
        instance.delete()

    def perform_update(self, serializer):
        instance = serializer.instance

        # Check if the requesting user is the creator of the post
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to update this post.")

        # Perform the update
        serializer.save()


class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.none()  # An empty queryset as we only handle creation
    serializer_class = AnalyticsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Analytics.objects.none()


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.select_related("user").all()
    permission_classes = (IsAuthenticated,)
