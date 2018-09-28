# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import Response, status
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from authority.permission import key as KeyPermission
from timeline.decorator import decorator_api
from deveops.api import WebTokenAuthentication
from .. import models,serializers,filter

__all__ = [
    "KeyListAPI", "KeyCreateAPI", "KeyUpdateAPI",
    "KeyDeleteAPI", 'KeyPagination', 'KeyListByPageAPI'
]


class KeyPagination(PageNumberPagination):
    page_size = 10


class KeyListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyListRequiredMixin, IsAuthenticated]
    filter_class = filter.KeyFilter


class KeyListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyListRequiredMixin, IsAuthenticated]
    pagination_class = KeyPagination
    filter_class = filter.KeyFilter


class KeyCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    permission_classes = [KeyPermission.KeyCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.KeyCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Key_KEY_CREATE'])
    def create(self, request, *args, **kwargs):
        response = super(KeyCreateAPI, self).create(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name,
            NAME = response.data['name'],
            UUID = response.data['uuid'],
        ), response


class KeyUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.KeyUpdateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Key_KEY_UPDATE'])
    def update(self, request, *args, **kwargs):
        key = self.get_object()
        response = super(KeyUpdateAPI, self).update(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name,
            NAME = key.name,
            UUID = key.uuid
        ), response


class KeyDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.KeyDeleteAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Key_KEY_DELETE'])
    def delete(self, request, *args, **kwargs):
        key = self.get_object()
        try:
            group = key.group
            return '', Response({'detail': u'该密钥属于应用组'+group.name+u'无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            response = super(KeyDeleteAPI,self).delete(request,*args,**kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                NAME=key.name,
                UUID=key.uuid
            ), response
