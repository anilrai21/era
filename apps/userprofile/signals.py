from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=UserProfile)
def send_authentication_emails(sender, instance, created, **kwargs):

    if created:
        instance.send_authentication_email()


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    """Create a user profile whenever a user object is created."""
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)
