# Generated by Django 4.0.4 on 2022-06-02 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_cart_is_paid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItems',
            new_name='CartItem',
        ),
    ]
