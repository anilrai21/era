# Generated by Django 2.2 on 2022-02-19 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0014_auto_20210316_2128"),
    ]

    operations = [
        migrations.CreateModel(
            name="Code",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=10)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "type",
                    models.CharField(
                        choices=[("flat", "FLAT"), ("percent", "PERCENT")],
                        max_length=10,
                    ),
                ),
                ("active", models.BooleanField(default=False)),
            ],
        ),
    ]
