# Generated by Django 5.1.1 on 2024-11-11 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_address_orderitem_order"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderitem",
            old_name="Product",
            new_name="product",
        ),
        migrations.AlterField(
            model_name="product",
            name="inventory",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]
