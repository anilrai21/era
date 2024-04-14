from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Category, CustomerOrder, Item
from .serializers import (
    CategorySerializer,
    CustomerOrderSerializer,
    ItemSerializer,
)


class CategoryViewSet(ModelViewSet):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "alias"
    search_fields = ("name", "alias")

    filter_backends = (SearchFilter,)


class ItemViewSet(ModelViewSet):
    model = Item
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    lookup_field = "alias"
    search_fields = ("name", "alias")
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        data = self.request.query_params

        listed = data.get("listed")

        queryset = self.queryset

        if listed == "True":
            queryset = Item.objects.listed()

        return queryset


class CustomerOrderViewSet(ModelViewSet):
    model = CustomerOrder
    serializer_class = CustomerOrderSerializer
    queryset = CustomerOrder.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ("name", "alias")
    filter_backends = (SearchFilter,)

    # queryset = CustomerOrder.objects.all().order_by('created')
    #
    # def get_queryset(self):
    #     order_by = self.request.query_params.get('order_by', '-created')
    #     return CustomerOrder.objects.all().order_by(order_by)
    #
