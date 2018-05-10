# -*- coding:utf-8 -*-
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import Response, status
from rest_framework.pagination import PageNumberPagination
from authority.permission import jumper as JumperPermission
from deveops.api import WebTokenAuthentication


__all__ = [
    "JumperListAPI", "JumperCreateAPI", "JumperUpdateAPI",
    "JumperDeleteAPI", 'JumperPagination', 'JumperListByPage'
]


class JumperPagination(PageNumberPagination):
    page_size = 10


class JumperListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperListRequiredMixin, IsAuthenticated]


class JumperListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperListRequiredMixin, IsAuthenticated]
    pagination_class = JumperPagination


class JumperStatusAPI(WebTokenAuthentication, generics.ListAPIView):
    serializer_class = serializers.JumperSerializer
    permission_classes = [AllowAny,]

    def get_object(self):
        return models.Jumper.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.check_status()
        obj.save()
        return Response({'detail': '刷新成功'}, status=status.HTTP_200_OK)


class JumperCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    permission_classes = [JumperPermission.JumperCreateRequiredMixin, IsAuthenticated]


class JumperUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'


class JumperDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        jumper = self.get_object()
        # jumper = models.Jumper.objects.get(id=int(kwargs['pk']))
        try:
            group = jumper.group
            return Response({'detail': u'该密钥属于应用组' + group.name + u'无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            return super(JumperDeleteAPI,self).delete(request,*args,**kwargs)
