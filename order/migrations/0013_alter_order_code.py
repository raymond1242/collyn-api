# Generated by Django 4.2.14 on 2024-09-08 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0012_order_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="code",
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]