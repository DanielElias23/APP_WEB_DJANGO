# Generated by Django 5.1.4 on 2025-02-17 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_brands_categories_customers_order_items_orders_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='manager_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
