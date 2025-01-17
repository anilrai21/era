# Generated by Django 2.2 on 2021-03-16 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_auto_20210316_2106"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="clearance",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="propertyname",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
    ]
