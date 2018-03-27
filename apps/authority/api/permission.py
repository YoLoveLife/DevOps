# -*- coding:utf-8 -*-
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from authority.permission import permission as PermissionPermission

__all__ = [
    "PermissionListAPI"
]


class PermissionListAPI(generics.ListAPIView):
    module = Permission
    serializer_class = serializers.PermissionSerializer
    queryset = Permission.objects.filter(codename__istartswith="yo_")
    permission_classes = [PermissionPermission.PermissionListRequiredMixin,IsAuthenticated]
