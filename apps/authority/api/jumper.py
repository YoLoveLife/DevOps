# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.views import Response, status
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from deveops.api import WebTokenAuthentication
from authority.permission import jumper as JumperPermission
from timeline.decorator import decorator_api
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
        return Response({'detail': '已进入刷新列表'}, status=status.HTTP_200_OK)


class JumperCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    permission_classes = [JumperPermission.JumperCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.JumperCreateAPI

    @decorator_api(timeline_type = settings.TIMELINE_KEY_VALUE['Jumper_JUMPER_CREATE'])
    def create(self, request, *args, **kwargs):
        response = super(JumperCreateAPI, self).create(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name,
            NAME = response.data['name'],
            UUID = response.data['uuid'],
            CONNECT_IP = response.data['connect_ip']
        ), response


class JumperUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.JumperUpdateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Jumper_JUMPER_UPDATE'])
    def update(self, request, *args, **kwargs):
        response = super(JumperUpdateAPI, self).update(request, *args, **kwargs)
        jumper = self.get_object()
        return self.msg.format(
            USER=request.user.full_name,
            NAME=jumper.name,
            UUID=jumper.uuid,
            CONNECT_IP=jumper.connect_ip
        ), response


class JumperDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    queryset = models.Jumper.objects.all()
    permission_classes = [JumperPermission.JumperDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.JumperDeleteAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Jumper_JUMPER_DELETE'])
    def delete(self, request, *args, **kwargs):
        jumper = self.get_object()
        try:
            group = jumper.group
            return '', Response({'detail': u'该密钥属于应用组' + group.name + u'无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            response = super(JumperDeleteAPI,self).delete(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                NAME=jumper.name,
                UUID=jumper.uuid,
                CONNECT_IP=jumper.connect_ip
            ), response
