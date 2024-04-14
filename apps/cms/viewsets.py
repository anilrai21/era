from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import CarouselImage
from .serializers import CarouselImageSerializer


class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all().order_by("order")
    serializer_class = CarouselImageSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
