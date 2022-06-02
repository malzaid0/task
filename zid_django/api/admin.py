from django.contrib import admin
from .models import Merchant, Customer, MerchantSetting, Cart, CartItems, Product, Language, ProductLangInfo

admin.site.register(Merchant)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(CartItems)
admin.site.register(MerchantSetting)
admin.site.register(Product)
admin.site.register(Language)
admin.site.register(ProductLangInfo)
