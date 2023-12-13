from django.core.exceptions import PermissionDenied
from django.db import models
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
    permission_classes = (IsAuthenticated, )

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


class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        # Perform the analytics calculation here
        analytics_data = Like.objects.filter(created_at__range=[date_from, date_to]).aggregate(
            likes_count=models.Count('id'),
            dislikes_count=models.Value(0, output_field=models.IntegerField())
        )

        dislikes_count = Dislike.objects.filter(created_at__range=[date_from, date_to]).aggregate(
            dislikes_count=models.Count('id')
        )

        analytics_data['dislikes_count'] = dislikes_count['dislikes_count']

        serializer = self.get_serializer(data=analytics_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.select_related("user").all()
    permission_classes = (IsAuthenticated,)
