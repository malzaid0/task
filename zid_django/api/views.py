from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import MerchantSetting
from .permissions import IsMerchant
from .serializers import (
    RegisterMerchantSerializer, RegisterCustomerSerializer, MyTokenObtainPairSerializer, TestSerializer,
    UpdateSettingsSerializer, CreateProductSerializer
)


class RegisterMerchant(CreateAPIView):
    serializer_class = RegisterMerchantSerializer


class RegisterCustomer(CreateAPIView):
    serializer_class = RegisterCustomerSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Test(CreateAPIView):
    serializer_class = TestSerializer


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
