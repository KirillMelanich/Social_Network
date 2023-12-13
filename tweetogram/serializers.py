from datetime import timedelta

from rest_framework import serializers
from .models import Post, Analytics, UserActivity, Like, Dislike


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
        read_only_fields = ("likes_count", "dislikes_count")

    def create(self, validated_data):
        date_from = validated_data.get("date_from")
        date_to = validated_data.get("date_to")

        # Perform the analytics calculation here. day_to is included to calculations
        likes_count = Like.objects.filter(
            created_at__range=[date_from, date_to + timedelta(days=1)]
        ).count()
        dislikes_count = Dislike.objects.filter(
            created_at__range=[date_from, date_to + timedelta(days=1)]
        ).count()

        # Add the calculated counts to the validated data
        validated_data["likes_count"] = likes_count
        validated_data["dislikes_count"] = dislikes_count

        # Create the Analytics instance
        return Analytics.objects.create(**validated_data)


class UserActivitySerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id", read_only=True)
    last_login = serializers.DateTimeField(source="user.last_login", read_only=True)

    class Meta:
        model = UserActivity
        fields = ("user_id", "last_login", "last_activity")
