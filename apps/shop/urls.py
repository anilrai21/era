from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.HomeView.as_view(),
        name="home_view",
    ),
    path(
        "about",
        views.AboutView.as_view(),
        name="about_view",
    ),
    path(
        "search",
        views.SearchView.as_view(),
        name="search_view",
    ),
    path(
        "contact-us",
        views.ContactUsView.as_view(),
        name="contact_us_view",
    ),
    path(
        "item/<slug:alias>",
        views.ItemDetailView.as_view(),
        name="item_detail_view",
    ),
    path(
        "products",
        views.ItemListView.as_view(),
        name="item_list_view",
    ),
    path(
        "place-order",
        views.PlaceOrderView.as_view(),
        name="place_order_view",
    ),
    path(
        "confirm-place-order",
        views.ConfirmMessagePlaceOrder.as_view(),
        name="confirm_message_place_order_view",
    ),
]
