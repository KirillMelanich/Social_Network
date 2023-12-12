from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from tweetogram.models import UserActivity


@receiver(post_save, sender=User)
# Creates a profile instance right after new user is registered
def create_user_activity(sender, instance, created, **kwargs):
    if created and not UserActivity.objects.filter(user=instance).exists():
        UserActivity.objects.create(user=instance)