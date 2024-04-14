# Generated by Django 2.2 on 2021-03-16 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0002_carouselimage_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contenttext",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="footer",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="navigation",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="navigationlink",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
    ]
