# Generated by Django 4.2.14 on 2024-08-15 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_alter_order_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]