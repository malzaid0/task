import phonenumbers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Merchant, Customer, MerchantSetting, Product, Language, ProductLangInfo, Cart, CartItem


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, "merchant_obj"):
            token["role"] = "Merchant"
        elif hasattr(user, "customer_obj"):
            token["role"] = "Customer"
        else:
            token["role"] = None
        return token


class RegisterMerchantSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(min_length=2)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)

    class Meta:
        model = Merchant
        fields = ["store_name", "email", "password", "access_token"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        new_user = User(username=validated_data["email"], email=validated_data["email"])
        new_user.set_password(validated_data["password"])
        new_user.save()
        Merchant.objects.create(user=new_user, store_name=validated_data["store_name"])
        validated_data["access_token"] = MyTokenObtainPairSerializer.get_token(new_user).access_token
        return validated_data


class RegisterCustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=2, max_length=100, allow_null=False, allow_blank=False)

    class Meta:
        model = Customer
        fields = ["phone", "email", "password", "access_token", "name"]

    def validate_phone(self, value):
        phone = f"+966{value[-9:]}"
        phone_validator = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(phone_validator):
            raise serializers.ValidationError("Invalid phone number")
        if Customer.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("phone already exists")
        return phone

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        new_user = User(
            username=validated_data["email"],
            email=validated_data["email"],
            first_name=validated_data["name"]
        )
        new_user.set_password(validated_data["password"])
        new_user.save()
        Customer.objects.create(user=new_user, phone=validated_data["phone"])
        validated_data["access_token"] = MyTokenObtainPairSerializer.get_token(new_user).access_token
        return validated_data


class UpdateSettingsSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(min_length=2)
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=False, min_value=0)

    class Meta:
        model = MerchantSetting
        fields = ["store_name", "price_include_vat", "vat_percentage", "shipping_cost"]
        extra_kwargs = {
            "price_include_vat": {"required": True},
            "vat_percentage": {"required": True},
        }

    def validate(self, attrs):
        if not attrs["price_include_vat"] and not attrs["vat_percentage"]:
            raise serializers.ValidationError(
                {"vat_percentage": "you need to set a vat percentage if the vat isn't included in the product price"})
        return attrs

    def update(self, instance, validated_data):
        merchant = self.context["request"].user.merchant_obj
        merchant.store_name = validated_data.get("store_name", merchant.store_name)
        merchant.save()
        instance.price_include_vat = validated_data["price_include_vat"]
        instance.vat_percentage = validated_data["vat_percentage"] if not validated_data["price_include_vat"] else 0
        instance.shipping_cost = validated_data["shipping_cost"]
        instance.save()
        return validated_data


class OtherLanguagesSerializer(serializers.Serializer):
    language = serializers.CharField(min_length=2, max_length=2)
    title = serializers.CharField(min_length=2)
    description = serializers.CharField(allow_null=True, allow_blank=True)

    def validate_language(self, value):
        if not Language.objects.filter(abbreviation__iexact=value).exists():
            raise serializers.ValidationError(f"{value} language isn't supported")
        return value


class ProductSerializer(serializers.ModelSerializer):
    internationals = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["seller"]

    def get_internationals(self, obj):
        values = []
        for info in obj.internationals.all():
            values.append({
                "language": info.language.abbreviation,
                "title": info.title,
                "description": info.description
            })
        return values


class CreateProductSerializer(serializers.ModelSerializer):
    internationals = OtherLanguagesSerializer(many=True, write_only=True)

    class Meta:
        model = Product
        fields = ["title", "description", "price", "inventory", "internationals"]
        extra_kwargs = {
            "description": {"required": True}
        }

    def create(self, validated_data):
        merchant = self.context["request"].user.merchant_obj
        other_languages = validated_data.pop("internationals")
        new_product = Product.objects.create(seller=merchant, **validated_data)
        for info in other_languages:
            lang_name = info.pop("language")
            language = Language.objects.filter(abbreviation__iexact=lang_name).last()
            ProductLangInfo.objects.create(language=language, product=new_product, **info)
        return new_product

    def to_representation(self, instance):
        return ProductSerializer(instance).data


class CartItemSerializer(serializers.ModelSerializer):
    item = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["item", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    totals = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ["is_paid", "customer"]

    def get_totals(self, obj):
        total_no_vat = 0
        vat = 0
        cart_items = obj.items.all()
        shipping = 0
        if cart_items:
            merchant = cart_items[0].item.seller
            store_settings = merchant.settings.last()
            if not store_settings:
                store_settings = MerchantSetting.objects.create(merchant=merchant, price_include_vat=True,
                                                                vat_percentage=0, shipping_cost=0)
            shipping = float(store_settings.shipping_cost) if store_settings.shipping_cost else 0
            for cart_item in cart_items:
                item_qty_total = float(cart_item.item.price * cart_item.quantity)
                if store_settings.price_include_vat:
                    current = item_qty_total / 1.15
                    total_no_vat += current
                    vat += item_qty_total - current
                else:
                    total_no_vat += item_qty_total
                    vat += item_qty_total * (float(store_settings.vat_percentage) / 100)
        return {
            "total_no_vat": float(str(round(total_no_vat, 2))),
            "vat": float(str(round(vat, 2))),
            "shipping": shipping,
            "total": total_no_vat + vat + shipping
        }


class AddToCartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ["item", "quantity"]

    def validate(self, attrs):
        if attrs["item"].inventory < attrs["quantity"]:
            raise serializers.ValidationError({"quantity": "not enough inventory"})
        return attrs

    def create(self, validated_data):
        customer = self.context["request"].user.customer_obj
        cart, _ = Cart.objects.get_or_create(customer=customer, is_paid=False)
        current = CartItem.objects.filter(cart=cart, item=validated_data["item"]).last()
        if current:
            current.quantity = validated_data["quantity"]
            current.save()
            return current
        else:
            new_cart_item = CartItem.objects.create(cart=cart, **validated_data)
            return new_cart_item

    def to_representation(self, instance):
        return CartSerializer(instance.cart).data
