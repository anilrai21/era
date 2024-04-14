from django.db import models

from ..shop.lib import get_valid_alias
from .constants import NAVIGATION_TYPE, SOCIAL_MEDIA
from .managers import SocialMediaManager


class CarouselImage(models.Model):
    carousel_image_id = models.AutoField(primary_key=True)
    text = models.TextField(default="", blank=True)
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to="carousel/")
    order = models.IntegerField(
        default=0,
    )

    _serializable = ("image",)

    class Meta:
        verbose_name_plural = "carousel image"
        db_table = "carousel_image"

    def __str__(self):
        return f"{self.carousel_image_id}-{self.image.url}"


class ContentManagement(models.Model):
    content_management_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    footer = models.ForeignKey(
        "Footer", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "content management"
        db_table = "content_management"

    def __str__(self):
        return f"{self.name}"


class ContentText(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    content = models.TextField()
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)


class Footer(models.Model):
    footer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    heading = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name_plural = "footer content"
        db_table = "footer_content"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)


class Navigation(models.Model):
    navigation_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
    )
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    navigation_type = models.CharField(
        max_length=2,
        choices=NAVIGATION_TYPE,
    )

    class Meta:
        verbose_name_plural = "navigation"
        db_table = "navigation"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)


class NavigationLink(models.Model):
    navigation_link_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
    )
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    url = models.CharField(
        max_length=255,
    )
    page = models.ForeignKey(
        "Page",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "navigation link"
        db_table = "navigation_link"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)

    # TODO: set a save that creates a page template


class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    # content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)


class SocialMedia(models.Model):
    social_media_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=20,
        choices=SOCIAL_MEDIA,
    )
    display_text = models.TextField(default="")
    link = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    display_in_footer = models.BooleanField(default=False)

    objects = SocialMediaManager()

    class Meta:
        verbose_name_plural = "social media"
        db_table = "social_media"

    def __str__(self):
        return f"{self.name}"

    def foundation_icon_class_name(self):
        return f"ft-social-{self.name}"
