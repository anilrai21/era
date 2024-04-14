from rest_framework import serializers

from .models import (
    Address,
    CartItem,
    Category,
    Customer,
    CustomerOrder,
    Image,
    Item,
    ItemPropertyTextValue,
    PropertyName,
    Purchase,
)


class PropertyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyName
        fields = ("name", "alias", "required")


class CategorySerializer(serializers.ModelSerializer):
    property_name = PropertyNameSerializer(many=True)

    class Meta:
        model = Category
        fields = Category.serializable() + ("property_name",)


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = Image.serializable()


class ItemPropertyTextValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPropertyTextValue
        fields = ItemPropertyTextValue.serializable()


class ItemListedSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(read_only=True, many=True)
    itempropertytextvalue_set = ItemPropertyTextValueSerializer(
        read_only=True, many=True
    )

    class Meta:
        model = Item
        fields = Item.serializable() + ("images", "itempropertytextvalue_set")


class ItemNotListedSerializer(serializers.ModelSerializer):
    active_status = serializers.CharField()
    image_status = serializers.CharField()
    saleprice_status = serializers.CharField()
    itempropertytextvalue_set = ItemPropertyTextValueSerializer(
        read_only=True, many=True
    )

    class Meta:
        model = Item
        fields = Item.serializable() + (
            "active_status",
            "image_status",
            "saleprice_status",
            "itempropertytextvalue_set",
        )


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemListedSerializer(read_only=True, many=False)

    class Meta:
        model = CartItem
        fields = ("item", "number")


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("user", "item", "number", "active", "purchased")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("user", "first_name", "last_name", "email", "phone_number")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "address1",
            "address2",
            "city",
            "province",
            "description",
            "address_text",
        )


class CustomerOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True, many=False)
    address = AddressSerializer(read_only=True, many=False)

    class Meta:
        model = CustomerOrder
        fields = (
            "id",
            "customer",
            "total_price",
            "bill",
            "address",
            "status",
            "active",
            "created",
            "modified",
        )


# class BackendItemPurchaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Purchase
#         fields = ('number', 'price', 'created', 'modified')


class BackendItemSerializer(serializers.ModelSerializer):
    # purchases = BackendItemPurchaseSerializer(read_only=True, many=True)
    images = ItemImageSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=False)

    class Meta:
        model = Item
        fields = (
            "category",
            "name",
            "alias",
            "sku",
            "number_of_items",
            "description",
            "active",
            "images",
            "current_price",
        )


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("number", "price", "created", "modified")


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)

    class Meta:
        model = Item
        fields = (
            "name",
            "alias",
            "category",
            "sku",
            "number_of_items",
            "description",
            "active",
            "created",
            "modified",
        )
