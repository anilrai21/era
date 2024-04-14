from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile_view"),
    path(
        "create-item",
        views.ProfileItemCreateView.as_view(),
        name="profile_item_create_view",
    ),
    path(
        "delete-item/<slug:alias>",
        views.ProfileItemDeleteView.as_view(),
        name="profile_item_delete_view",
    ),
    path(
        "create-category",
        views.ProfileCategoryCreateView.as_view(),
        name="profile_category_create_view",
    ),
    path(
        "registration-complete/<slug:token>",
        views.RegistrationCompleteView.as_view(),
        name="registration_complete_view",
    ),
    path(
        "registration-completed-message",
        views.RegistrationCompleteMessageView.as_view(),
        name="registration_complete_message_view",
    ),
    path(
        "registration-failed-message",
        views.RegistrationFailedMessageView.as_view(),
        name="registration_failed_message_view",
    ),
    path(
        "registered-already-message",
        views.RegisteredAlreadyMessageView.as_view(),
        name="registered_already_view",
    ),
    path(
        "resend-email-confirmation-message",
        views.ResendEmailConfirmationMessage.as_view(),
        name="resend_email_confirmation_message_view",
    ),
    path("cart", views.CartView.as_view(), name="cart_view"),
    path(
        "listed-items",
        views.ProfileListedItem.as_view(),
        name="listed_item_view",
    ),
    path(
        "not-listed-items",
        views.ProfileNotListedItem.as_view(),
        name="not_listed_item_view",
    ),
    path("category", views.CategoryView.as_view(), name="category_view"),
    path(
        "category/<slug:alias>",
        views.CategoryDetailView.as_view(),
        name="category_detail_view",
    ),
    path(
        "category/delete/<slug:alias>",
        views.CategoryDeleteView.as_view(),
        name="category_delete_view",
    ),
    path(
        "purchased-items",
        views.PurchasedItemsView.as_view(),
        name="purchased_items_view",
    ),
    path(
        "customer-order",
        views.CustomerOrdersListView.as_view(),
        name="customer_order_list_view",
    ),
    path(
        "customer-order/<int:pk>",
        views.CustomerOrderDetailView.as_view(),
        name="customer_order_detail_view",
    ),
    path(
        "item/detail/<slug:alias>",
        views.ItemDetailView.as_view(),
        name="item_detail_view",
    ),
    path(
        "update-price/<slug:alias>",
        views.UpdateSalePriceView.as_view(),
        name="update_sale_price_view",
    ),
    path("cms", views.CMSView.as_view(), name="cms_view"),
]
