from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User

from apps.core.forms import ClassInputForm

from .models import (
    Address,
    Category,
    ContactMessage,
    Customer,
    CustomerOrder,
    CustomerOrderItem,
    Image,
    Item,
    SalePrice,
)


class CategoryForm(ClassInputForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "active")


class ContactMessageForm(ClassInputForm, forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = ContactMessage
        fields = ("email", "subject", "message")


class ItemCreateForm(ClassInputForm, forms.ModelForm):
    image_1 = forms.ImageField(required=True)
    image_2 = forms.ImageField(required=False)
    image_3 = forms.ImageField(required=False)
    price = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        # only change attributes if an instance is passed
        instance = kwargs.get("instance")
        if instance:
            image_list = instance.images.all().order_by("order")
            self.base_fields["price"].initial = instance.current_price

            print("IMAGE", image_list)
            if len(image_list) > 0:
                print("IMAGE 1", image_list[0])
                self.base_fields["image_1"].initial = image_list[0]
            if len(image_list) > 1:
                self.base_fields["image_2"].initial = image_list[1]
            if len(image_list) > 2:
                self.base_fields["image_3"].initial = image_list[2]
        super().__init__(*args, **kwargs)

    class Meta:
        model = Item

        fields = (
            "name",
            "category",
            "sku",
            "number_of_items",
            "description",
            "active",
        )

    def save(self, commit=False):
        """
        Create the `Item` instance and take the `image` and `price` from
        cleaned_data to create Image and SalePrice instances, respectively
        for the created `Item` instance.
        """
        item = super(ItemCreateForm, self).save(commit=False)
        item.save()

        data = self.cleaned_data

        if data.get("image_1"):
            Image.objects.create(
                item=item, image=data["image_1"], active=True, order=100
            )

        if data.get("image_2"):
            Image.objects.create(
                item=item, image=data["image_2"], active=True, order=200
            )

        if data.get("image_3"):
            Image.objects.create(
                item=item, image=data["image_3"], active=True, order=300
            )

        SalePrice.objects.create(item=item, active=True, price=data["price"])

        return item


class OrderForm(ClassInputForm, forms.Form):
    first_name = forms.CharField(
        required=True,
    )
    last_name = forms.CharField(
        required=True,
    )
    email = forms.EmailField(
        required=True,
    )
    phone_number = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={"type": "number"}),
    )
    address1 = forms.CharField(
        required=True,
    )
    address2 = forms.CharField()
    city = forms.CharField(
        required=True,
    )
    province = forms.CharField(
        required=True,
    )
    description = forms.CharField()

    def get_address_and_customer(self, cleaned_data):
        """
        Take cleaned_data that we get from this form and use it to get the
        Address and Customer instances

        return: Address and Customer instances
        """

        address, status = Address.objects.get_or_create(
            address1=cleaned_data.get("address1"),
            address2=cleaned_data.get("address2"),
            city=cleaned_data.get("city"),
            province=cleaned_data.get("province"),
            description=cleaned_data.get("description", ""),
        )
        user = User.objects.filter(email=cleaned_data.get("email")).first()
        customer, status = Customer.objects.get_or_create(
            first_name=cleaned_data.get("first_name"),
            last_name=cleaned_data.get("last_name"),
            phone_number=cleaned_data.get("phone_number"),
            email=cleaned_data.get("email"),
            user=user,
        )

        return address, customer

    def create_customer_order(
        self, address, customer, items, discount_type, discount_amount
    ):
        """
        Create a CustomerOrder and CustomerOrderItem instance using Address,
        Customer and Item instances

        return: instance of CustomerOrder
        """
        total_price = 0

        customer_order = CustomerOrder.objects.create(
            customer=customer,
            address=address,
            total_price=0,
            active=True,
        )

        for item, quantity, price in items:
            total_price = total_price + (quantity * price)
            CustomerOrderItem.objects.create(
                order=customer_order,
                item=item,
                number=quantity,
                price=price,
            )

        if discount_type == "flat":
            total_discount = discount_amount
        elif discount_type == "percent":
            total_discount = discount_amount * total_price / 100
        else:
            total_discount = 0

        total_price = total_price - total_discount

        customer_order.total_price = total_price
        customer_order.save()

        return customer_order


class SalePriceForm(ClassInputForm, forms.ModelForm):
    class Meta:
        model = SalePrice
        fields = ("item", "active", "price")
