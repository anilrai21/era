from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import CarouselImage


class CarouselImageCreateView(CreateView):
    template_name = "ecommerce/profile/cms/carousel_image_create.html"
    model = CarouselImage
    fields = ("image", "order")
    success_url = reverse_lazy("profile:cms_view")
    queryset = CarouselImage.objects.all()
