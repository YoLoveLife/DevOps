# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.views import Response, status
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from deveops.api import WebTokenAuthentication
from authority.permission import jumper as JumperPermission
from .. import models,serializers,filter


__all__ = [
    "JumperListAPI", "JumperCreateAPI", "JumperUpdateAPI",
    "JumperDeleteAPI", 'JumperPagination', 'JumperListByPageAPI',
]


class JumperPagination(PageNumberPagination):
    page_size = 10


class JumperListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperListRequiredMixin, IsAuthenticated]
    filter_class = filter.JumperFilter


class JumperListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperListRequiredMixin, IsAuthenticated]
    pagination_class = JumperPagination
    filter_class = filter.JumperFilter


class JumperStatusAPI(WebTokenAuthentication, APIView):
    permission_classes = [JumperPermission.JumperStatusRequiredMixin, IsAuthenticated]

    def get_object(self):
        return models.Jumper.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.check_status()
        return Response({'detail': '刷新成功'}, status=status.HTTP_200_OK)


class JumperCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    permission_classes = [JumperPermission.JumperCreateRequiredMixin, IsAuthenticated]


class JumperUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
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
        try:
            group = jumper.group
            return Response({'detail': u'该密钥属于应用组' + group.name + u'无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            return super(JumperDeleteAPI,self).delete(request,*args,**kwargs)
