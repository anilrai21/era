from rest_framework.routers import DefaultRouter

from .viewsets import CarouselImageViewSet

router = DefaultRouter()
router.register(r"carousel-image", CarouselImageViewSet)
