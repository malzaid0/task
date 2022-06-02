import phonenumbers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import Merchant, Customer, MerchantSetting, Product, Language, ProductLangInfo


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

    class Meta:
        model = Customer
        fields = ["phone", "email", "password", "access_token"]

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
        new_user = User(username=validated_data["email"], email=validated_data["email"])
        new_user.set_password(validated_data["password"])
        new_user.save()
        Customer.objects.create(user=new_user, phone=validated_data["phone"])
        validated_data["access_token"] = MyTokenObtainPairSerializer.get_token(new_user).access_token
        return validated_data


class TestSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["token"]

    def create(self, validated_data):
        tok = RefreshToken.for_user(User.objects.last())
        validated_data["token"] = tok.access_token
        return validated_data


class UpdateSettingsSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(min_length=2)
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=False, min_value=0)

    class Meta:
        model = MerchantSetting
        fields = ["store_name", "price_include_vat", "vat_percentage", "shipping_cost"]

    def validate(self, attrs):
        if not attrs["price_include_vat"] and not attrs["vat_percentage"]:
            raise serializers.ValidationError(
                {"vat_percentage": "you need to set a vat percentage if the vat isn't included in the product price"})
        return attrs

    def update(self, instance, validated_data):
        merchant = self.context["request"].user.merchant_obj
        if validated_data["store_name"] != merchant.store_name:
            merchant.store_name = validated_data["store_name"]
            merchant.save()
        instance.price_include_vat = validated_data["price_include_vat"]
        instance.vat_percentage = validated_data["vat_percentage"] if not validated_data["price_include_vat"] else 0
        instance.shipping_cost = ["shipping_cost"]
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


class CreateProductSerializer(serializers.ModelSerializer):
    other_languages = OtherLanguagesSerializer(many=True)

    class Meta:
        model = Product
        fields = ["title", "description", "price", "inventory", "other_languages"]

    def create(self, validated_data):
        merchant = self.context["request"].user.merchant_obj
        other_languages = validated_data.pop("other_languages")
        new_product = Product.objects.create(seller=merchant, **validated_data)
        for info in other_languages:
            info_dict = dict(info)
            print(info, info_dict)
            lang_name = info_dict.pop("language")
            language = Language.objects.filter(abbreviation__iexact=lang_name).last()
            ProductLangInfo.objects.create(language=language, product=new_product, **info_dict)
        return validated_data
