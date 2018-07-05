# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from db import models,serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from db.permission import user as UserPermission


class DBUserPagination(PageNumberPagination):
    page_size = 10


class DBUserListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.User
    serializer_class = serializers.DBUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [UserPermission.DBUserListRequiredMixin, IsAuthenticated]
    filter_class = filter.DBUserFilter


class DBUserListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.User
    serializer_class = serializers.DBUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [UserPermission.DBUserListRequiredMixin, IsAuthenticated]
    pagination_class = DBUserPagination
    filter_class = filter.DBUserFilter


class DBUserCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.User
    serializer_class = serializers.DBUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [UserPermission.DBUserCreateRequiredMixin, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super(DBUserCreateAPI, self).create(request, *args, **kwargs)


class DBUserUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.User
    serializer_class = serializers.DBUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [UserPermission.DBUserUpdateRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class DBUserDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.User
    serializer_class = serializers.DBUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [UserPermission.DBUserDeleteRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        role = self.get_object()
        if role.users.exists():
            return Response({'detail':'当前角色下存在用户无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(DBUserDeleteAPI,self).delete(request, *args, **kwargs)