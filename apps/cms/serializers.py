from rest_framework import serializers

from .models import CarouselImage


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ("pk", "active", "image", "order")
        lookup_field = "pk"
