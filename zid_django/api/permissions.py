from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    message = "You must be a merchant"

    def has_permission(self, request, view):
        return hasattr(request.user, "merchant_obj")


class IsCustomer(BasePermission):
    message = "You must be a customer"

    def has_permission(self, request, view):
        return hasattr(request.user, "customer_obj")
