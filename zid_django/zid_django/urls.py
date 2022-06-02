"""zid_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from api import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/merchant/', views.RegisterMerchant.as_view()),
    path('register/customer/', views.RegisterCustomer.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('test/', views.Test.as_view()),

    path('merchant/update-info/', views.UpdateSettings.as_view()),
    path('merchant/add-product/', views.CreateProduct.as_view()),
]
