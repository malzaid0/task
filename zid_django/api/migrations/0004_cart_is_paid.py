# Generated by Django 4.0.4 on 2022-06-02 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_product_inventory_product_seller_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
