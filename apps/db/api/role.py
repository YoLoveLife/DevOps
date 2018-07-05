# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from db import models,serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.exceptions import ObjectDoesNotExist
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from db.permission import role as RolePermission

class DBRolePagination(PageNumberPagination):
    page_size = 10


class DBRoleListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Role
    serializer_class = serializers.DBRoleSerializer
    queryset = models.Role.objects.all()
    permission_classes = [RolePermission.DBRoleListRequiredMixin, IsAuthenticated]
    filter_class = filter.DBRoleFilter


class DBRoleListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Role
    serializer_class = serializers.DBRoleSerializer
    queryset = models.Role.objects.all()
    permission_classes = [RolePermission.DBRoleListRequiredMixin, IsAuthenticated]
    pagination_class = DBRolePagination
    filter_class = filter.DBRoleFilter


class DBRoleCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Role
    serializer_class = serializers.DBRoleSerializer
    queryset = models.Role.objects.all()
    permission_classes = [RolePermission.DBRoleCreateRequiredMixin, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            instance = models.Instance.objects.get(id=request.data['instance'])
            if instance.roles.filter(name=request.data['name']).exists():
                return Response({'detail': '当前角色名称已经在该实例中存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return super(DBRoleCreateAPI, self).create(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            return Response({'detail':'当前Instance已经被删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class DBRoleUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Role
    serializer_class = serializers.DBRoleSerializer
    queryset = models.Role.objects.all()
    permission_classes = [RolePermission.DBRoleUpdateRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class DBRoleDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Role
    serializer_class = serializers.DBRoleSerializer
    queryset = models.Role.objects.all()
    permission_classes = [RolePermission.DBRoleDeleteRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        role = self.get_object()
        if role.users.exists():
            return Response({'detail':'当前角色下存在用户无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(DBRoleDeleteAPI,self).delete(request, *args, **kwargs)