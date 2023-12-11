from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "content", "created_at", "likes", "dislikes")
        read_only_fields = ("author",)

    def get_likes(self, obj):
        return obj.get_likes_count()

    def get_dislikes(self, obj):
        return obj.get_dislikes_count()
