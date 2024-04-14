from typing import List, Union

from django.contrib.auth.models import User
from django.db import Error, models
from django.db.models import Q, Sum

from apps.core.models import TimestampAbstractModel

from .constants import (
    CODE_TYPE_CHOICES,
    CUSTOMER_ORDER_CHOICES,
    ITEM_LOG_TYPE,
    RETURN_TYPE,
)
from .lib import get_valid_alias
from .managers import CartItemManager, CategoryManager, ItemManager


class AbstractItemPropertyValueModel(models.Model):
    item_property_value_id = models.AutoField(primary_key=True)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    property_name = models.ForeignKey(
        "PropertyName",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.item}: {self.property_name.name} - {self.value}"


class Category(TimestampAbstractModel):
    """
    Category is used to differentiate the types of items

    PropertyName is attached to this model so two items with same category
    will have similar property names.

    """

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    active = models.BooleanField(default=False)
    property_name = models.ManyToManyField("PropertyName", blank=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "categories"
        db_table = "shop_category"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    _serializable = ("name", "alias", "active")


class Clearance(TimestampAbstractModel):
    clearance_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
    )
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    items = models.ManyToManyField(
        "Item",
    )
    image = models.ImageField(
        upload_to="gallery/",
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    effective_start_date = models.DateTimeField()
    effective_end_date = models.DateTimeField()
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "clearances"
        db_table = "shop_clearance"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)


class ContactMessage(TimestampAbstractModel):
    """
    Messages send directly to us.
    """

    contact_message = models.AutoField(primary_key=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        verbose_name_plural = "contact messages"
        db_table = "shop_contact_message"


class Image(TimestampAbstractModel):
    image_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="gallery/",
    )
    active = models.BooleanField(default=False)
    order = models.IntegerField()

    class Meta:
        verbose_name_plural = "images"
        db_table = "shop_image"

    def __str__(self):
        return f"{self.item.name}-image"

    _serializable = ("image", "order")


class Item(TimestampAbstractModel):
    """
    Item is any product that we are buying and selling.

    Listed
    * Item are the items that are ready for sale.
    * The necessary fields are
        - `active` field True
        - has a `saleprice` with `active` field True
        - has an `image` with `active` field True

    Not Listed
    * Item that are not ready for various reasons above.

    Images
    * Item can have multiple images.
    * The main image will be considered with the image that comes first when
      arranged in ascending order the field `order`

    Sale price
    * Item can have multiple sale prices related to `SalePrice` model
    * The `SalePrice` instance with `active` field True will be current price

    """

    item_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=255)
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    sku = models.CharField(max_length=6, unique=True)
    number_of_items = models.IntegerField()
    description = models.TextField(default="")
    active = models.BooleanField(default=False)

    objects = ItemManager()

    _serializable = (
        "name",
        "alias",
        "category_name",
        "sku",
        "number_of_items",
        "description",
        "active",
    )

    class Meta:
        verbose_name_plural = "items"
        db_table = "shop_item"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)

    def add_purchased_numbers(self, purchased_number: int) -> None:
        self.number_of_items = self.number_of_items + purchased_number
        self.save()

    def subtract_purchase_returned_numbers(self, returned_number: int) -> None:
        self.number_of_items = self.number_of_items - returned_number
        self.save()

    def main_image_url(self) -> Union[None, str]:
        return self.images.order_by("order").first().image.url

    def minor_images_urls(self) -> List:
        return [image.image.url for image in self.images.order_by("order")[1:]]

    def current_price(self) -> float:
        return self.saleprice_set.get(active=True).price

    def available_item(self):
        current_ordered_number = CustomerOrderItem.objects.filter(
            Q(item=self) & Q(order__active=True) & ~Q(order__status__in=[])
        ).aggregate(Sum("number"))
        return self.number_of_items

    def check_if_available(self, expected_number) -> bool:
        difference = self.available_item() - expected_number
        if difference >= 0:
            return True
        else:
            return False

    @property
    def category_name(self):
        return self.category.name


class ItemDisposal(TimestampAbstractModel):
    item_disposal_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        "Item",
        on_delete=models.CASCADE,
    )
    number = models.IntegerField()
    notes = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "item disposals"
        db_table = "shop_item_disposal"

    def __str__(self):
        return f"{self.item.name}-disposal-{self.number}"


class ItemLog(TimestampAbstractModel):
    item_log_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="item_logs"
    )
    number_of_items = models.IntegerField()
    log_type = models.CharField(max_length=2, choices=ITEM_LOG_TYPE)

    class Meta:
        verbose_name_plural = "item logs"
        db_table = "shop_itemlog"

    def __str__(self):
        return f"{self.item.name}-{self.item_log_id}"


class PropertyName(TimestampAbstractModel):
    property_name_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    alias = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    active = models.BooleanField(default=False)
    required = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "property names"
        db_table = "shop_propertyname"

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = get_valid_alias(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ItemPropertyBooleanValue(
    TimestampAbstractModel, AbstractItemPropertyValueModel
):
    value = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "item property boolean value"
        db_table = "shop_itemproperty_boolean_value"


class ItemPropertyTextValue(
    TimestampAbstractModel, AbstractItemPropertyValueModel
):
    value = models.TextField()

    class Meta:
        verbose_name_plural = "item property text value"
        db_table = "shop_itemproperty_text_value"

    _serializable = (
        "property_name",
        "value",
    )


class ItemPropertyDecimalValue(
    TimestampAbstractModel, AbstractItemPropertyValueModel
):
    value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )

    class Meta:
        verbose_name_plural = "item property decimal value"
        db_table = "shop_itemproperty_decimal_value"


class ItemPropertyIntegerValue(
    TimestampAbstractModel, AbstractItemPropertyValueModel
):
    value = models.IntegerField()

    class Meta:
        verbose_name_plural = "item property integer value"
        db_table = "shop_itemproperty_integer_value"


class Purchase(TimestampAbstractModel):
    purchase_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="purchases"
    )
    number = models.IntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name_plural = "purchases"
        db_table = "shop_purchase"

    def __str__(self):
        return f"{self.item.name}-purchase-{self.purchase_id}"

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)

        # Adding purchased number to the item and creating ItemLog
        self.item.add_purchased_numbers(purchased_number=self.number)
        ItemLog.objects.create(
            item=self.item, number_of_items=self.number, log_type="pu"
        )

    def do_purchase_return(self, return_type, number_of_items, description=""):
        """
        Create and return a PurchaseReturn for this Purchase
        """
        return PurchaseReturn.objects.create(
            purchase=self,
            return_type=return_type,
            number_of_items=number_of_items,
            description=description,
        )


class PurchaseReturn(TimestampAbstractModel):
    """
    the purchase model is a `purchase` for us, not for a customer.
    """

    purchase_return_id = models.AutoField(primary_key=True)
    purchase = models.ForeignKey(
        "Purchase", on_delete=models.CASCADE, related_name="purchase_returns"
    )
    description = models.TextField(default="")
    return_type = models.CharField(
        max_length=10,
        choices=RETURN_TYPE,
        default=RETURN_TYPE["full"],
    )
    number_of_items = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        verbose_name_plural = "purchase returns"
        db_table = "shop_purchase_return"

    def __str__(self):
        return (
            f"{self.purchase.item.name}-purchase-return-"
            f"{self.purchase_return_id}"
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # subtract returned items in the purchase
        self.purchase.item.subtract_purchase_returned_numbers(
            returned_number=self.purchase.number
        )

        ItemLog.objects.create(
            item=self.purchase.item,
            number_of_items=self.number_of_items,
            log_type="pr",
        )


class Sale(TimestampAbstractModel):
    """
    the sale model is a `sale` for us so it is a purchase for a customer.
    """

    sale_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="sales"
    )
    number = models.IntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name_plural = "sales"
        db_table = "shop_sale"

    def __str__(self):
        return f"{self.item.name}-sales-{self.sale_id}"

    def save(self, *args, **kwargs):
        item = self.item
        item.number_of_items = item.number_of_items - self.number

        if item.number_of_items > 0:
            super(self.__class__, self).save(*args, **kwargs)
            item.save()

            ItemLog.objects.create(item=item, number_of_items=self.number)
        else:
            raise Error


class SaleReturn(TimestampAbstractModel):
    sale_return_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(
        "Sale", on_delete=models.CASCADE, related_name="sale_returns"
    )

    class Meta:
        verbose_name_plural = "sales returns"
        db_table = "shop_sale_return"

    def __str__(self):
        return f"{self.sale.item.name}-purchase-{self.sale_return_id}"


class SalePrice(TimestampAbstractModel):
    sale_price_id = models.AutoField(primary_key=True)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name_plural = "sale prices"
        db_table = "shop_sale_price"

    def save(self, *args, **kwargs):
        self.set_item_sale_price_inactive()
        return super(self.__class__, self).save(*args, **kwargs)

    def set_item_sale_price_inactive(self) -> None:
        self.item.saleprice_set.exclude(pk=self.pk).update(active=False)


class Customer(TimestampAbstractModel):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
    )
    last_name = models.CharField(
        max_length=255,
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"


class CustomerOrder(TimestampAbstractModel):
    """
    Orders Placed by the Customers.

    Active CustomerOrder has its field `active` as True.

    """

    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    bill = models.FileField(
        upload_to="customer_orders",
        null=True,
        blank=True,
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=20,
        choices=CUSTOMER_ORDER_CHOICES,
        default=CUSTOMER_ORDER_CHOICES["started"],
    )
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.customer.email} {self.total_price}"


class CustomerOrderItem(TimestampAbstractModel):
    """
    This model defines the order, items, number and price.

    """

    order = models.ForeignKey(
        "CustomerOrder",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        "Item",
        on_delete=models.CASCADE,
    )
    number = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self):
        return

    def __str__(self):
        return f"{self.order.id} {self.item.name}"


class Address(TimestampAbstractModel):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    description = models.TextField(
        default="",
        blank=True,
    )

    def __str__(self):
        return self.address_text()

    def address_text(self):
        if self.address2:
            address = f"{self.address1}, {self.address2}"
        else:
            address = self.address1
        return f"{address}, {self.city}, {self.province}"


class CartItem(TimestampAbstractModel):
    customer = models.OneToOneField(
        "Customer",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    purchased = models.BooleanField(default=False)

    objects = CartItemManager()

    def __str__(self):
        return f"{self.item.name}"


class PurchasedItem(TimestampAbstractModel):
    customer = models.OneToOneField(
        "Customer",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    returned = models.BooleanField(default=False)


class WishList(TimestampAbstractModel):
    customer = models.OneToOneField(
        "Customer",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    purchased = models.BooleanField(default=False)


class Code(models.Model):
    code = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=10, choices=CODE_TYPE_CHOICES)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code}"

    _serializable = ("pk", "active", "code", "amount", "type")
