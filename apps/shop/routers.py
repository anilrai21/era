from rest_framework.routers import DefaultRouter

from .viewsets import CategoryViewSet, CustomerOrderViewSet, ItemViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"item", ItemViewSet)
router.register(r"category", CategoryViewSet)
router.register(r"customer-order", CustomerOrderViewSet)
