# Generated by Django 4.2.14 on 2024-11-21 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0013_alter_order_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=models.CharField(blank=True, default="", max_length=12),
        ),
    ]