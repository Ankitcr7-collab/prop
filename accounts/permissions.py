from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import BasePermission
from .models import UserRoles

# class IsModeratorAuthenticated(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.user == UserRoles.objects(user = request.user).is_moderator == True
    

class IsModeratorAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role.is_moderator)