from django.contrib import admin

from .models import (
    Address,
    CartItem,
    Category,
    Code,
    ContactMessage,
    CustomerOrder,
    CustomerOrderItem,
    Image,
    Item,
    ItemLog,
    ItemPropertyBooleanValue,
    ItemPropertyDecimalValue,
    ItemPropertyIntegerValue,
    ItemPropertyTextValue,
    PropertyName,
    Purchase,
    PurchaseReturn,
    Sale,
    SalePrice,
    SaleReturn,
)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "customer",
        "total_price",
        "bill",
        "address",
        "status",
        "active",
    )


@admin.register(CustomerOrderItem)
class CustomerOrderItemAdmin(admin.ModelAdmin):
    list_display = ("pk", "order", "item", "number", "price")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ContactMessage.serializable()


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = Image.serializable()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = Item.serializable()


@admin.register(PropertyName)
class PropertyNameAdmin(admin.ModelAdmin):
    list_display = PropertyName.serializable()


@admin.register(ItemPropertyBooleanValue)
class ItemPropertyBooleanValueAdmin(admin.ModelAdmin):
    list_display = ItemPropertyBooleanValue.serializable()


@admin.register(ItemPropertyDecimalValue)
class ItemPropertyDecimalValueAdmin(admin.ModelAdmin):
    list_display = ItemPropertyDecimalValue.serializable()


@admin.register(ItemPropertyIntegerValue)
class ItemPropertyIntegerValueAdmin(admin.ModelAdmin):
    list_display = ItemPropertyIntegerValue.serializable()


@admin.register(ItemPropertyTextValue)
class ItemPropertyTextValueAdmin(admin.ModelAdmin):
    list_display = ItemPropertyTextValue.serializable()


@admin.register(ItemLog)
class ItemLogAdmin(admin.ModelAdmin):
    list_display = ItemLog.serializable()


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("purchase_id", "item", "number", "price")


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_return_id",
        "purchase",
        "description",
        "return_type",
        "number_of_items",
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = Sale.serializable()


@admin.register(SalePrice)
class SalePriceAdmin(admin.ModelAdmin):
    list_display = SalePrice.serializable()


@admin.register(SaleReturn)
class SaleReturnAdmin(admin.ModelAdmin):
    list_display = SaleReturn.serializable()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = CartItem.serializable()


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = Code._serializable
