# Generated by Django 4.2.14 on 2024-09-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0009_rename_delivered_order_has_delivery"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="has_topper",
            field=models.BooleanField(default=False),
        ),
    ]
