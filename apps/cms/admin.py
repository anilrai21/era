from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import CarouselImage, ContentText


@admin.register(ContentText)
class ContentTextAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)


# @admin.register(Carousel)
# class CarouselAdmin(admin.ModelAdmin):
#     summernote_fields = Carousel._serializable


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    summernote_fields = CarouselImage._serializable
