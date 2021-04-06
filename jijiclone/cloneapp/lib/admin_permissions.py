from rest_framework import permissions
from ..models import Seller


class IsUserSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        try:
            user_instance = Seller.objects.get(email=user)
        except:
            return False

        if user_instance.is_admin or user_instance.is_superadmin:
            return True
        return False
