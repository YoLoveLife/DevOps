# -*- coding:utf-8 -*-
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import Response, status
from rest_framework.pagination import PageNumberPagination
from authority.permission import key as KeyPermission
from deveops.api import WebTokenAuthentication


__all__ = [
    "KeyListAPI", "KeyCreateAPI", "KeyUpdateAPI",
    "KeyDeleteAPI", 'KeyPagination', 'KeyListByPage'
]


class KeyPagination(PageNumberPagination):
    page_size = 10


class KeyListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyListRequiredMixin, IsAuthenticated]


class KeyListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyListRequiredMixin, IsAuthenticated]
    pagination_class = KeyPagination


class KeyCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    permission_classes = [KeyPermission.KeyCreateRequiredMixin, IsAuthenticated]


class KeyUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyUpdateRequiredMixin, IsAuthenticated]


class KeyDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyDeleteRequiredMixin, IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        key = models.Key.objects.get(id=int(kwargs['pk']))
        if key.group is not None:
            return Response({'detail': u'该密钥属于应用组'+key.group_name+u'无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(KeyDeleteAPI,self).delete(request,*args,**kwargs)
