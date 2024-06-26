# Generated by Django 4.2.13 on 2024-05-17 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("currency_code", models.PositiveIntegerField()),
                (
                    "buy_rate",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=10, null=True
                    ),
                ),
                (
                    "sell_rate",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=10, null=True
                    ),
                ),
                (
                    "cross_rate",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=10, null=True
                    ),
                ),
                ("last_update", models.DateTimeField()),
            ],
        ),
    ]
