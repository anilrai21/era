import uuid

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models

from apps.core.models import TimestampAbstractModel
from apps.shop.models import Item
from config.settings.base import EMAIL_HOST_USER

from .managers import UserProfileManager


class UserProfile(TimestampAbstractModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(max_length=20, blank=True, default="")
    email_authenticated = models.BooleanField(default=False)
    authentication_code = models.CharField(
        max_length=64, unique=True, default=uuid.uuid4
    )

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

    def send_authentication_email(self):
        subject = "Registration"
        message = self.message()
        send_mail(subject, message, EMAIL_HOST_USER, [self.user.email])

    def message(self) -> str:
        return (
            f"Hi!\n\n"
            f"Thank you for registering with us.\n"
            f"Ignore this email if you have changed your mind or don't "
            f"recognize this.\n"
            f"Click this to complete registration.\n"
            f"https://kipaprints.com/profile/registration-complete/"
            f"{self.authentication_code}\n\n"
            f"Thanks,\n"
            f"Kipa Prints Team"
        )

    def make_authenticated(self):
        self.email_authenticated = True
        self.save()

    @property
    def is_authenticated(self) -> bool:
        """ """
        if self.user.is_authenticated and self.email_authenticated:
            return True
        else:
            return False
