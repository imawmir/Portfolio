# Generated by Django 5.1.1 on 2024-11-12 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_remove_order_ordered_orderitem_ordered"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="ordered",
            field=models.BooleanField(default=False),
        ),
    ]
