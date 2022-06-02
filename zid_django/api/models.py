from django.db import models
from django.contrib.auth.models import User


class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name="merchant_obj")
    store_name = models.CharField(max_length=100)

    def __str__(self):
        return self.store_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name="customer_obj")
    phone = models.CharField(max_length=20)


class MerchantSetting(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="settings")
    price_include_vat = models.BooleanField(default=True)
    vat_percentage = models.PositiveSmallIntegerField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)


class Product(models.Model):
    seller = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveSmallIntegerField()


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
