import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from apps.cms.models import CarouselImage, ContentText
from apps.core.constants import PAGINATION_NUMBER

from .constants import ABOUT_MESSAGE
from .display_messages import (
    CONTACT_US_SOME_ERROR_MESSAGE,
    CONTACT_US_THANK_YOU_MESSAGE,
)
from .forms import ContactMessageForm, OrderForm
from .models import Item


class HomeView(TemplateView):
    """
    This is the main landing page for the website
    """

    template_name = "ecommerce/home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["items"] = Item.objects.all()
        data["latest_items"] = Item.objects.with_property_values(latest=True)
        data["non_latest_items"] = Item.objects.with_property_values(
            latest=False
        )
        data["carousel_data"] = CarouselImage.objects.filter(
            active=True
        ).order_by("order")
        return data


class AboutView(TemplateView):
    """
    This is the about page for the website
    """

    template_name = "ecommerce/about.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        about = ContentText.objects.filter(name__iexact="about")
        if about.count() > 0:
            data["about_text"] = about.first().content
        else:
            # TODO: Add default text later
            data["about_text"] = ABOUT_MESSAGE

        return data


class SearchView(TemplateView):
    template_name = "ecommerce/search.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        default_lowest_price = 0
        default_highest_price = Item.objects.get_highest_price()

        searched_term: str = self.request.GET.get("search_term", None)
        category: str = self.request.GET.get("category", None)
        page_number: int = self.request.GET.get("page", 1)
        order: str = self.request.GET.get("order", "price_ascending")
        lowest_price: int = self.request.GET.get(
            "lower_price", default_lowest_price
        )
        highest_price: int = self.request.GET.get(
            "highest_price", default_highest_price
        )

        items: QuerySet = Item.objects.search(
            value=searched_term, category_name=category
        )

        if order == "price_ascending":
            items = items.order_by("current_price")
        elif order == "price_descending":
            items = items.order_by("-current_price")

        items = items.filter(
            Q(current_price__gte=lowest_price)
            & Q(current_price__lte=highest_price)
        )

        paginated_items = Paginator(items, PAGINATION_NUMBER).page(page_number)
        data["query_params"] = f"?search_term={searched_term}&page="
        data["items"] = paginated_items
        data["num_pages"] = paginated_items.paginator.num_pages
        data["searched_term"] = searched_term
        data["searched_category"] = category
        data["lowest_price"] = lowest_price
        data["highest_price"] = highest_price
        data["order"] = order

        return data


class ItemDetailView(TemplateView):
    template_name = "ecommerce/item_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        alias: str = kwargs.get("alias")
        data["item"] = Item.objects.get(alias=alias)

        return data


class ContactUsView(View):
    template_name = "ecommerce/contact_us.html"

    def get(self, request, *args, **kwargs):
        contact_form = ContactMessageForm()
        context = {"contact_form": contact_form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        contact_form = ContactMessageForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, CONTACT_US_THANK_YOU_MESSAGE)
            return render(request, self.template_name)
        else:
            messages.error(request, CONTACT_US_SOME_ERROR_MESSAGE)
            return redirect("shop:contact_us_view")


class ItemListView(TemplateView):
    template_name = "ecommerce/item_list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        product_type = self.request.GET.get("product-type")
        page_number: int = self.request.GET.get("page", 1)

        items: QuerySet = Item.objects.listed()

        if product_type:
            items = items.filter(category__alias=product_type)

        paginated_items = Paginator(items, PAGINATION_NUMBER).page(page_number)

        default_lowest_price = 0
        default_highest_price = Item.objects.get_highest_price()

        data["items"] = paginated_items
        data["num_pages"] = paginated_items.paginator.num_pages
        data["query_params"] = "?page="
        # data['pages'] = range(paginated_items.paginator.num_pages)
        # print("paginated_items", paginated_items.paginator.num_pages)
        # print(paginated_items.paginator.__dict__)
        data["lowest_price"] = default_lowest_price
        data["highest_price"] = default_highest_price
        data["order"] = "price_ascending"

        return data


class PlaceOrderView(View):
    def get(self, request, *args, **kwargs):
        """
        Entering the details for the orders.
        """
        # data = request.GET
        # aliases = data.keys()
        # items = Item.objects.filter(alias__in=aliases)
        #
        # items_list = [{
        #     "name": item.name,
        #     "count": data[item.alias],
        #     "alias": item.alias,
        #     "main_image_url": item.main_image_url(),
        #     "current_price": item.current_price()
        # } for item in items]
        #
        order_form = OrderForm()
        context = {
            "order_form": order_form,
        }
        return render(
            request, "ecommerce/orders/place_order.html", context=context
        )

    def post(self, request, *args, **kwargs):
        """
        Confirming that the order details are okay.
        """
        form = OrderForm(request.POST)
        form.is_valid()
        address, customer = form.get_address_and_customer(
            cleaned_data=form.cleaned_data
        )

        item_list_string = request.POST.get("item_list")

        if item_list_string:
            item_list = json.loads(item_list_string)

            ordered_item_list = [
                (
                    Item.objects.get(alias=item["alias"]),
                    int(item["quantity"]),
                    float(item["price"]),
                )
                for item in item_list
            ]

            discount_amount = request.POST.get("discountAmount", 0)

            if type(discount_amount) and discount_amount != "":
                try:
                    discount_amount = int(discount_amount)
                except ValueError:
                    discount_amount = 0

            discount_type = request.POST.get("discountType", "")

            customer_order = form.create_customer_order(
                address=address,
                customer=customer,
                items=ordered_item_list,
                discount_type=discount_type,
                discount_amount=discount_amount,
            )

            context = {"customer_order": customer_order}

            return render(
                request, "ecommerce/orders/place_order.html", context=context
            )
        return render(request, "ecommerce/orders/place_order.html")


class ConfirmMessagePlaceOrder(View):
    def post(self, request, *args, **kwargs):
        """
        Confirm Message for the Place Order
        """
        return render(request, "ecommerce/orders/confirm_place_order.html")
