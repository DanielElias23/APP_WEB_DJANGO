# Generated by Django 5.1.4 on 2025-02-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_brands_brand_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='id',
        ),
        migrations.AlterField(
            model_name='customers',
            name='customer_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
