from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Post, Like, Dislike, UserActivity
from django.utils import timezone

User = get_user_model()


@receiver(post_save, sender=Post)
def update_user_activity_on_post_create(sender, instance, created, **kwargs):
    if created:
        user_activity, created = UserActivity.objects.get_or_create(
            user=instance.author
        )
        user_activity.last_activity = timezone.now()
        user_activity.save()


@receiver(post_save, sender=Like)
@receiver(post_save, sender=Dislike)
def update_user_activity_on_like_or_dislike_create(sender, instance, created, **kwargs):
    if created:
        user_activity, created = UserActivity.objects.get_or_create(user=instance.user)
        user_activity.last_activity = timezone.now()
        user_activity.save()
