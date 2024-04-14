from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "carouse-image/create",
        views.CarouselImageCreateView.as_view(),
        name="carousel_image_create_view",
    ),
]
