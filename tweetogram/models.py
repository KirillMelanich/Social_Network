from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def like(self, user):
        Like.objects.create(user=user, post=self)
        self.likes += 1
        self.save()

    def dislike(self, user):
        Dislike.objects.create(user=user, post=self)
        self.dislikes += 1
        self.save()

    def get_likes_count(self):
        return self.likes

    def get_dislikes_count(self):
        return self.dislikes


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Analytics(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)


class UserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(null=True, blank=True)
    last_token_refresh = models.DateTimeField(null=True, blank=True)
    registration_time = models.DateTimeField(auto_now_add=True)

    def get_last_activity(self):
        last_post_created_at = Post.objects.filter(author=self.user).aggregate(
            last_post_created_at=Max("created_at")
        )["last_post_created_at"]
        last_like_created_at = Like.objects.filter(author=self.user).aggregate(
            last_like_created_at=Max("created_at")
        )["last_like_created_at"]
        last_dislike_created_at = Dislike.objects.filter(author=self.user).aggregate(
            last_dislike_created_at=Max("created_at")
        )["last_dislike_created_at"]

        last_action = max(
            last_post_created_at, last_like_created_at, last_dislike_created_at
        )

        self.last_activity = last_action

        self.save()

    def update_last_token_redresh(self):
        self.last_token_refresh = timezone.now()
        self.save()

    def get_registration_time(self):
        return self.registration_time


