from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.paginators import EraPagination

from .models import CartItem, Code, CustomerOrder, Item, Purchase
from .serializers import (
    BackendItemSerializer,
    CartItemCreateSerializer,
    CartItemSerializer,
    CustomerOrderSerializer,
    ItemNotListedSerializer,
    ItemSerializer,
    PurchaseSerializer,
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CartItemListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = CartItem
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        query = CartItem.objects.list(user=user)
        return query


class CartItemAddAPIView(CreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    model = CartItem
    serializer_class = CartItemCreateSerializer


class CustomerOrderListAPIView(ListAPIView):
    """
    CustomerOrder List API that are active (have their `active` field as True)
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CustomerOrderSerializer
    # queryset = CustomerOrder.objects.all().order_by('created')

    def get_queryset(self):
        order_by = self.request.query_params.get("order_by", "-created")
        return CustomerOrder.objects.all().order_by(order_by)


class BackendItemDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    model = Item
    serializer_class = BackendItemSerializer
    queryset = (
        Item.objects.with_current_price().prefetch_related("purchases").all()
    )
    lookup_field = "alias"


class BackendPurchaseListAPIView(ListAPIView):
    """
    Purchase list for backend use only
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    model = Purchase
    serializer_class = PurchaseSerializer
    pagination_class = EraPagination

    def get_queryset(self):
        item_alias = self.request.query_params.get("item_alias")
        if item_alias:
            return Purchase.objects.filter(item__alias=item_alias)
        else:
            return Purchase.objects.all()


class ItemListAPIView(ListAPIView):
    """
    Item list
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    model = Item
    serializer_class = ItemSerializer
    # pagination_class = EraPagination

    def get_queryset(self):
        listed = self.request.query_params.get("listed", True)
        if listed is not False or listed != "false":
            return Item.objects.listed().order_by("-created")
        else:
            return Item.objects.not_listed().order_by("-created")


class ItemNotListedAPIView(ListAPIView):
    serializer_class = ItemNotListedSerializer
    queryset = Item.objects.not_listed()


class GetCodeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")
        code_instance = Code.objects.filter(active=True, code=code).first()
        if code_instance:
            data = {"amount": code_instance.amount, "type": code_instance.type}
        else:
            data = {}
        return Response(data=data)
