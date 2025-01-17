# Generated by Django 2.2 on 2020-06-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0010_auto_20200529_2218"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchasereturn",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="purchasereturn",
            name="number_of_items",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="purchasereturn",
            name="return_type",
            field=models.CharField(
                choices=[("full", "Full"), ("partial", "Partial")],
                default="Full",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="customerorder",
            name="status",
            field=models.CharField(
                choices=[
                    ("started", "Order Started"),
                    ("dispatched", "Order Dispatched"),
                    ("delivered", "Order Delivered"),
                    ("cancelled", "Order Cancelled"),
                    ("returned_started", "Order Returned Started"),
                    ("returned_completed", "Order Returned"),
                    ("unknown", "Order Unknown"),
                    ("lost", "Order Lost"),
                ],
                default="Order Started",
                max_length=20,
            ),
        ),
    ]
