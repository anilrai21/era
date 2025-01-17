# Generated by Django 2.2 on 2020-02-16 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "category_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "alias",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "categories",
                "db_table": "shop_category",
            },
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "contact_message",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField()),
            ],
            options={
                "verbose_name_plural": "contact messages",
                "db_table": "shop_contact_message",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "alias",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("sku", models.CharField(max_length=6, unique=True)),
                ("number_of_items", models.IntegerField()),
                ("description", models.TextField(default="")),
                ("active", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="shop.Category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "items",
                "db_table": "shop_item",
            },
        ),
        migrations.CreateModel(
            name="PropertyName",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "property_name_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "alias",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("active", models.BooleanField(default=False)),
                ("required", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "item property",
                "db_table": "shop_itemproperty",
            },
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "purchase_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("number", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="shop.Item",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "purchases",
                "db_table": "shop_purchase",
            },
        ),
        migrations.CreateModel(
            name="Sale",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "sale_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("number", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales",
                        to="shop.Item",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "sales",
                "db_table": "shop_sale",
            },
        ),
        migrations.CreateModel(
            name="SaleReturn",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "sale_return_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_returns",
                        to="shop.Sale",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "sales returns",
                "db_table": "shop_sale_return",
            },
        ),
        migrations.CreateModel(
            name="SalePrice",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "sale_price_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("active", models.BooleanField(default=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.Item",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "sale prices",
                "db_table": "shop_sale_price",
            },
        ),
        migrations.CreateModel(
            name="PurchaseReturn",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "purchase_return_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "purchase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_returns",
                        to="shop.Purchase",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "purchase returns",
                "db_table": "shop_purchase_return",
            },
        ),
        migrations.CreateModel(
            name="ItemPropertyTextValue",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_property_value_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("value", models.TextField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.Item",
                    ),
                ),
                (
                    "property_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.PropertyName",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "item property text value",
                "db_table": "shop_itemproperty_text_value",
            },
        ),
        migrations.CreateModel(
            name="ItemPropertyIntegerValue",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_property_value_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("value", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.Item",
                    ),
                ),
                (
                    "property_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.PropertyName",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "item property integer value",
                "db_table": "shop_itemproperty_integer_value",
            },
        ),
        migrations.CreateModel(
            name="ItemPropertyDecimalValue",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_property_value_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.Item",
                    ),
                ),
                (
                    "property_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.PropertyName",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "item property decimal value",
                "db_table": "shop_itemproperty_decimal_value",
            },
        ),
        migrations.CreateModel(
            name="ItemPropertyBooleanValue",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_property_value_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("value", models.BooleanField(default=False)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.Item",
                    ),
                ),
                (
                    "property_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.PropertyName",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "item property boolean value",
                "db_table": "shop_itemproperty_boolean_value",
            },
        ),
        migrations.CreateModel(
            name="ItemLog",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_log_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("number_of_items", models.IntegerField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("pu", "Purchases"),
                            ("sl", "Sales"),
                            ("pr", "Purchase Return"),
                            ("sr", "Sales Return"),
                            ("di", "Item Disposed"),
                            ("dr", "Item Disposed Reversed"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_logs",
                        to="shop.Item",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "item logs",
                "db_table": "shop_itemlog",
            },
        ),
        migrations.CreateModel(
            name="ItemDisposal",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "item_disposal_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("number", models.IntegerField()),
                ("notes", models.TextField()),
                ("active", models.BooleanField(default=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.Item",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "item disposals",
                "db_table": "shop_item_disposal",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "image_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("image", models.ImageField(upload_to="gallery/")),
                ("active", models.BooleanField(default=False)),
                ("order", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="shop.Item",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "images",
                "db_table": "shop_image",
            },
        ),
        migrations.CreateModel(
            name="Clearance",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "clearance_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "alias",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("image", models.ImageField(upload_to="gallery/")),
                (
                    "discount",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("effective_start_date", models.DateTimeField()),
                ("effective_end_date", models.DateTimeField()),
                ("active", models.BooleanField(default=False)),
                ("items", models.ManyToManyField(to="shop.Item")),
            ],
            options={
                "verbose_name_plural": "clearances",
                "db_table": "shop_clearance",
            },
        ),
        migrations.AddField(
            model_name="category",
            name="property_name",
            field=models.ManyToManyField(to="shop.PropertyName"),
        ),
    ]
