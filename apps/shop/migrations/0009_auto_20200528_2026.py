# Generated by Django 2.2 on 2020-05-28 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_customerorderitem_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerorder",
            name="bill",
            field=models.FileField(
                blank=True, null=True, upload_to="customer_orders"
            ),
        ),
    ]