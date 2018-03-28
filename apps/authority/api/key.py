# -*- coding:utf-8 -*-
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import Response, status
from authority.permission import key as KeyPermission

__all__ = [
    "KeyListAPI", "KeyCreateAPI", "KeyUpdateAPI",
    "KeyDeleteAPI"
]


class KeyListAPI(generics.ListAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyListRequiredMixin, IsAuthenticated]

class KeyCreateAPI(generics.CreateAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    permission_classes = [KeyPermission.KeyCreateRequiredMixin, IsAuthenticated]


class KeyUpdateAPI(generics.UpdateAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyUpdateRequiredMixin, IsAuthenticated]


class KeyDeleteAPI(generics.DestroyAPIView):
    module = models.Key
    serializer_class = serializers.KeySerializer
    queryset = models.Key.objects.all()
    permission_classes = [KeyPermission.KeyDeleteRequiredMixin, IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        key = models.Key.objects.get(id=int(kwargs['pk']))
        if key.group.exists():
            return Response({'detail': '该密钥属于应用组'+key.group_name+'无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(KeyDeleteAPI,self).delete(request,*args,**kwargs)
