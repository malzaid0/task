from django.db import models
from django.contrib.auth.models import User


class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    store_name = models.CharField(max_length=100)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)


class MerchantSetting(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="settings")
    price_include_vat = models.BooleanField()
    vat_percentage = models.PositiveSmallIntegerField()
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_updated = models.DateTimeField(auto_now=True)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Language(models.Model):
    abbreviation = models.CharField(max_length=2)


class ProductLangInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="internationals")
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    class Meta:
        unique_together = ("product", "language")


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name="carts")
    date_created = models.DateTimeField(auto_now_add=True)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveSmallIntegerField()
    price_at_checkout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
