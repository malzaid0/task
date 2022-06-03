from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import MerchantSetting, Cart
from .permissions import IsMerchant, IsCustomer
from .serializers import (
    RegisterMerchantSerializer, RegisterCustomerSerializer, MyTokenObtainPairSerializer, UpdateSettingsSerializer,
    CreateProductSerializer, CartSerializer, AddToCartSerializer
)


class RegisterMerchant(CreateAPIView):
    serializer_class = RegisterMerchantSerializer


class RegisterCustomer(CreateAPIView):
    serializer_class = RegisterCustomerSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UpdateSettings(RetrieveUpdateAPIView):
    queryset = MerchantSetting.objects.all()
    serializer_class = UpdateSettingsSerializer
    permission_classes = [IsAuthenticated, IsMerchant]
    http_method_names = ["put"]

    def get_object(self):
        merchant = self.request.user.merchant_obj
        current = MerchantSetting.objects.filter(merchant=merchant).last()
        if current:
            return current
        else:
            return MerchantSetting.objects.create(merchant=merchant)


class CreateProduct(CreateAPIView):
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated, IsMerchant]


class GetCart(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_object(self):
        customer = self.request.user.customer_obj
        cart = customer.carts.filter(is_paid=False).last()
        if cart:
            return cart
        return Cart.objects.create(customer=customer)


class AddToCart(CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
