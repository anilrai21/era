# Generated by Django 2.2 on 2021-03-16 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0012_auto_20201202_0032"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
    ]
