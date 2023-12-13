from rest_framework import serializers
from .models import Post, Analytics, UserActivity


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "content", "created_at", "likes", "dislikes")
        read_only_fields = ("author",)

    @staticmethod
    def get_likes(obj):
        return obj.get_likes_count()

    @staticmethod
    def get_dislikes(obj):
        return obj.get_dislikes_count()


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = ("date_from", "date_to", "likes_count", "dislikes_count")


class UserActivitySerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id", read_only=True)
    last_login = serializers.DateTimeField(source="user.last_login", read_only=True)

    class Meta:
        model = UserActivity
        fields = ("user_id", "last_login", "last_activity")
