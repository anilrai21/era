from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, TemplateView

from apps.shop.constants import ITEM_MESSAGE
from apps.shop.forms import CategoryForm, ItemCreateForm, SalePriceForm
from apps.shop.models import (
    Category,
    CustomerOrder,
    Item,
    ItemPropertyTextValue,
    PropertyName,
)

from .constants import AUTH_MESSAGES
from .forms import KipaAuthenticationForm, RegisterForm
from .models import UserProfile


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "ecommerce/profile/profile_home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["selector_name"] = "profile_home"

        return data


class ProfileItemCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        context = {"item_create_form": ItemCreateForm()}
        return render(
            request, "ecommerce/profile/items/item_add.html", context=context
        )

    def post(self, request, *args, **kwargs):
        key_prefix = "property__"
        request_post = request.POST
        form = ItemCreateForm(request_post or None, request.FILES or None)

        if form.is_valid():
            item = form.save()

            for key in request_post:
                if key_prefix in key:
                    value = request_post[key]
                    property_name = PropertyName.objects.get(
                        name=key.replace(key_prefix, "")
                    )
                    ItemPropertyTextValue.objects.create(
                        item=item, property_name=property_name, value=value
                    )
            messages.success(request, ITEM_MESSAGE["create_success"])
            return redirect("profile:listed_item_view")
        else:
            messages.error(request, ITEM_MESSAGE["create_fail"])
            return redirect("shop:home_view")


class ProfileCategoryCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        context = {"category_create_form": CategoryForm()}
        return render(
            request,
            "ecommerce/profile/items/category_add.html",
            context=context,
        )

    def post(self, request, *args, **kwargs):
        request_post = request.POST
        form = CategoryForm(request_post or None)

        if form.is_valid():
            category = form.save()

            for key in request_post:
                if "category_property_name" in key:
                    property_name = PropertyName.objects.create(
                        name=request_post[key]
                    )
                    category.property_name.add(property_name)

            messages.success(request, "CONTACT_US_THANK_YOU_MESSAGE")
            return redirect("profile:category_view")
        else:
            messages.error(request, "CONTACT_US_SOME_ERROR_MESSAGE")
            return redirect("shop:home_view")


class ProfileItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy("profile:listed_item_view")
    template_name = "ecommerce/profile/items/item_confirm_delete.html"

    def get_object(self):
        self.set_successful_url(from_url=self.request.GET.get("from_url"))

        alias = self.kwargs.get("alias")
        obj = self.model.objects.filter(alias=alias).first()
        return obj

    def set_successful_url(self, from_url):
        if from_url == "listed":
            self.success_url = reverse_lazy("profile:listed_item_view")
        else:
            self.success_url = reverse_lazy("profile:not_listed_item_view")


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {"form": form}
        return render(
            request, "ecommerce/authentication/register.html", context=context
        )

    def post(self, request, *args, **kwargs):
        request_post = request.POST
        form = RegisterForm(request_post or None)

        if form.is_valid():
            user = form.save()
            phone_number = request_post.get("phone_number", "")

            profile = user.userprofile
            profile.phone_number = phone_number
            profile.save()

            messages.success(request, "CREATED")
            return render(
                request,
                "ecommerce/authentication/message.html",
                {
                    "message": AUTH_MESSAGES["EMAIL_SENT"]["MESSAGE"],
                    "title": AUTH_MESSAGES["EMAIL_SENT"]["TITLE"],
                },
            )
        else:
            context = {"form": form}
            error_data = form.errors.as_data().values()

            messages.error(request, error_data)

            return render(
                request,
                "ecommerce/authentication/register.html",
                context=context,
            )


class KipaLoginView(LoginView):
    template_name = "ecommerce/authentication/login.html"
    redirect_authenticated_user = True
    form_class = KipaAuthenticationForm


class RegistrationCompleteView(View):
    def get(self, request, *args, **kwargs):
        token: str = kwargs["token"]

        try:
            profile = UserProfile.objects.get(authentication_code=token)

            if profile.email_authenticated:
                return redirect("profile:registered_already_view")
            elif (
                not profile.email_authenticated
                and token == profile.authentication_code
            ):
                profile.make_authenticated()
                return redirect("profile:registration_complete_message_view")
            else:
                return render(request, "ecommerce/errors/404.html")
        except UserProfile.DoesNotExist:
            return redirect("profile:email_registration_failed_message_view")


class RegistrationCompleteMessageView(TemplateView):
    template_name = "ecommerce/authentication/registration_completed.html"


class RegistrationFailedMessageView(TemplateView):
    template_name = "ecommerce/authentication/registration_failed.html"


class RegisteredAlreadyMessageView(TemplateView):
    template_name = "ecommerce/authentication/registered_already.html"


class ResendEmailConfirmationMessage(TemplateView):
    def get(self, request, *args, **kwargs):

        profile = request.user.userprofile
        profile.send_authentication_email()

        return render(
            request,
            "ecommerce/authentication/message.html",
            {
                "message": AUTH_MESSAGES["EMAIL_RESENT"]["MESSAGE"],
                "title": AUTH_MESSAGES["EMAIL_RESENT"]["TITLE"],
            },
        )


class CartView(TemplateView):
    template_name = "ecommerce/cart/cart.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        return {}


class ProfileListedItem(TemplateView):
    template_name = "ecommerce/profile/items/listed_item.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["selector_name"] = "listed_item"
        return data


class ProfileNotListedItem(TemplateView):
    template_name = "ecommerce/profile/items/not_listed_item.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["selector_name"] = "not_listed_item"
        return data


class CategoryView(TemplateView):
    template_name = "ecommerce/profile/items/category.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["selector_name"] = "category"
        return data


class CategoryDetailView(DetailView):
    model = Category
    template_name = "ecommerce/profile/items/category_detail.html"
    slug_field = "alias"
    slug_url_kwarg = "alias"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print(data)
        return data


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy("profile:category_view")
    template_name = "ecommerce/profile/items/category_confirm_delete.html"
    slug_url_kwarg = "alias"

    def get_object(self):
        alias = self.kwargs.get("alias")
        obj = self.model.objects.filter(alias=alias).first()
        return obj


class PurchasedItemsView(TemplateView):
    template_name = "ecommerce/profile/customer/purchased_items_list.html"


class CustomerOrdersListView(TemplateView):
    template_name = "ecommerce/profile/items/customer_orders_list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["selector_name"] = "customer_orders"
        return data


class CustomerOrderDetailView(LoginView, DetailView):
    template_name = "ecommerce/profile/items/customer_order_detail.html"
    model = CustomerOrder
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["selector_name"] = "customer_orders"
        return data


class ItemDetailView(LoginView, TemplateView):
    template_name = "ecommerce/profile/items/item_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        alias = kwargs.get("alias")
        from_url = self.request.GET.get("from_url")

        instance = (
            Item.objects.with_current_price()
            .prefetch_related("images")
            .filter(alias=alias)
            .get()
        )

        form = ItemCreateForm(
            self.request.POST or None,
            self.request.FILES or None,
            instance=instance,
        )

        data["alias"] = alias
        data["form"] = form
        data["from_url"] = from_url
        return data


class UpdateSalePriceView(View):
    def get(self, request, *args, **kwargs):
        alias: str = kwargs.get("alias")
        item = Item.objects.with_current_price().get(alias=alias)
        form = SalePriceForm()
        form.fields["price"].initial = item.current_price
        context = {
            "form": form,
            "item": item,
        }
        return render(
            request,
            "ecommerce/profile/items/item_price_update.html",
            context=context,
        )

    def post(self, request, *args, **kwargs):
        alias: str = kwargs.get("alias")
        form = SalePriceForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

        return redirect("profile:item_detail_view", alias=alias)


class CMSView(TemplateView):
    template_name = "ecommerce/profile/cms/cms.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["selector_name"] = "cms"
        return data
