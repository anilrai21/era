from django.db import models
from django.db.models import (
    Case,
    CharField,
    OuterRef,
    Q,
    QuerySet,
    Subquery,
    Value,
    When,
)

from .constants import LATEST_ITEMS, MANAGER_ERROR_MESSAGES


class CategoryManager(models.Manager):
    def active(self) -> QuerySet:
        return super().get_queryset().filter(Q(active=True))

    # TODO: search needs work
    def search(self) -> QuerySet:
        return super().get_queryset().filter(Q(active=True))


class ItemManager(models.Manager):
    def with_current_price(self):
        from .models import SalePrice

        return (
            super()
            .get_queryset()
            .prefetch_related("images")
            .annotate(
                current_price=Subquery(
                    SalePrice.objects.filter(
                        Q(active=True) & Q(item__pk=OuterRef("pk"))
                    ).values("price")[:1]
                )
            )
        )

    def listed(self) -> QuerySet:
        from .models import Image, SalePrice

        return (
            (
                super()
                .get_queryset()
                .prefetch_related("images")
                .filter(
                    Q(active=True)
                    & Q(saleprice__active=True)
                    & Q(images__active=True)
                )
                .annotate(
                    current_price=Subquery(
                        SalePrice.objects.filter(
                            Q(active=True) & Q(item__pk=OuterRef("pk"))
                        ).values("price")[:1]
                    )
                )
                .annotate(
                    main_image_url=Subquery(
                        Image.objects.filter(
                            Q(active=True) & Q(item__pk=OuterRef("pk"))
                        ).values("image")[:1]
                    )
                )
            )
            .order_by("-created")
            .distinct()
        )

    def not_listed(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .exclude(
                Q(active=True)
                & Q(saleprice__active=True)
                & Q(images__active=True)
            )
            .order_by("-created")
            .annotate(
                active_status=Case(
                    When(
                        active=False,
                        then=Value(MANAGER_ERROR_MESSAGES["NOT_ACTIVE"]),
                    ),
                    default=Value(MANAGER_ERROR_MESSAGES["DONE"]),
                    output_field=CharField(),
                ),
                saleprice_status=Case(
                    When(
                        saleprice=None,
                        then=Value(MANAGER_ERROR_MESSAGES["NO_SALE_PRICE"]),
                    ),
                    When(
                        saleprice__active=False,
                        then=Value(
                            MANAGER_ERROR_MESSAGES["NO_ACTIVE_SALE_PRICE"]
                        ),
                    ),
                    default=Value(MANAGER_ERROR_MESSAGES["DONE"]),
                    output_field=CharField(),
                ),
                image_status=Case(
                    When(
                        images=None,
                        then=Value(MANAGER_ERROR_MESSAGES["NO_IMAGES"]),
                    ),
                    When(
                        images__active=False,
                        then=Value(MANAGER_ERROR_MESSAGES["NO_ACTIVE_IMAGES"]),
                    ),
                    default=Value(MANAGER_ERROR_MESSAGES["DONE"]),
                    output_field=CharField(),
                ),
            )
        ).distinct()

    def latest_listed(
        self, number_of_latest_items: int = LATEST_ITEMS
    ) -> QuerySet:
        return self.listed().order_by("-created")[:number_of_latest_items]

    def non_latest_listed(
        self, number_of_latest_items: int = LATEST_ITEMS
    ) -> QuerySet:
        latest_listed = [
            x.item_id for x in self.latest_listed(number_of_latest_items)
        ]
        return self.listed().exclude(item_id__in=latest_listed)

    def search(self, value: str, category_name: str = "all") -> QuerySet:
        queryset: QuerySet = self.listed()
        # if category_name == 'all' or category_name == '':
        #     queryset = queryset.filter(
        #         Q(name__icontains=value) |
        #         Q(sku=value) |
        #         Q(description__iregex=value) |
        #         Q(itempropertytextvalue__value__iregex=value)
        #     )
        # else:
        #     queryset = queryset.filter(
        #         Q(name__icontains=value) |
        #         Q(sku=value) |
        #         Q(description__icontains=value)
        #     )
        #     queryset = queryset.filter(Q(category__name__icontains=value))
        queryset = queryset.filter(
            Q(name__icontains=value)
            | Q(sku=value)
            | Q(description__iregex=value)
            | Q(itempropertytextvalue__value__iregex=value)
        )
        if not (
            category_name == "all"
            or category_name == ""
            or category_name is None
        ):
            queryset = queryset.filter(
                Q(category__name__icontains=category_name)
            )

        return queryset.distinct()

    def with_property_values(self, latest: bool):
        """
        returns a list of dict with the properties defined in
        ItemPropertyTextValue where the value is not empty.
        """
        from .models import ItemPropertyTextValue

        props = ItemPropertyTextValue.objects.filter(~Q(value="")).values(
            "item_id", "value", "property_name__name"
        )

        items = (
            self.listed()
            .order_by("-created")
            .values(
                "item_id",
                "name",
                "category__name",
                "alias",
                "sku",
                "description",
                "number_of_items",
                "main_image_url",
                "current_price",
            )
        )

        if latest:
            items = items[:LATEST_ITEMS]
        else:
            items = items[LATEST_ITEMS:]

        for item in items:
            item_props = [
                prop for prop in props if item["item_id"] == prop["item_id"]
            ]
            item["item_props"] = item_props

        return items

    # TODO: add properties in annotation
    def properties(self):
        return self.get_queryset().annotate()

    def get_highest_price(self):
        item_with_highest_price = (
            self.listed().order_by("-current_price").first()
        )
        if item_with_highest_price:
            return item_with_highest_price.current_price


class CartItemManager(models.Manager):
    def active(self) -> QuerySet:
        return super().get_queryset().filter(Q(active=True))

    def list(self, user):
        return self.active().filter(user=user)
