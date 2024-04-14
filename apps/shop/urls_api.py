from django.urls import include, path

from .routers import router
from .views_api import (
    BackendItemDetailAPIView,
    BackendPurchaseListAPIView,
    CustomerOrderListAPIView,
    GetCodeAPIView,
    ItemListAPIView,
    ItemNotListedAPIView,
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "not-listed-items",
        ItemNotListedAPIView.as_view(),
        name="not-listed-item-api",
    ),
    path(
        "customer-order/list",
        CustomerOrderListAPIView.as_view(),
        name="customer_orders_list_api_view",
    ),
    path(
        "item/backend-detail/<slug:alias>",
        BackendItemDetailAPIView.as_view(),
        name="backend_item_detail_api_view",
    ),
    path(
        "purchase/backend-list",
        BackendPurchaseListAPIView.as_view(),
        name="backend_purchase_list_api_view",
    ),
    path("item/list", ItemListAPIView.as_view(), name="item_list_api_view"),
    path(
        "code/retrieve/<slug:code>", GetCodeAPIView.as_view(), name="get_code"
    ),
]
