# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from django.conf import settings
from timeline.decorator import decorator_api
from ..permission import codework as CodeWorkPermission
from deveops.api import WebTokenAuthentication
from rest_framework.views import APIView

__all__ = [
    'CodeWorkCheckAPI', 'CodeWorkCreateAPI', 'CodeWorkListByPageAPI',
    'CodeWorkPagination', 'CodeWorkRunAPI', 'CodeWorkStatusAPI'
]


class CodeWorkPagination(PageNumberPagination):
    page_size = 10


class CodeWorkListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkSerializer
    queryset = models.Code_Work.objects.all().order_by('-id')
    permission_classes = [CodeWorkPermission.CodeWorkListRequiredMixin, IsAuthenticated]
    pagination_class = CodeWorkPagination
    filter_class = filter.CodeWorkFilter


class CodeWorkCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkSerializer
    permission_classes = [CodeWorkPermission.CodeWorkCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.CodeWorkCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Code_Work_CODEWORK_CREATE'])
    def create(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(CodeWorkCreateAPI, self).create(request, *args, **kwargs)
            obj = models.Code_Work.objects.get(id=response.data['id'], uuid=response.data['uuid'])
            return self.msg.format(
                USER=request.user.full_name,
                MISSION=obj.mission.info,
                REASON=obj.info,
                UUID=obj.uuid,
            ), response
        else:
            return '', self.qrcode_response


# Base Class
class CodeWorkStatusAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkStatusSerializer
    permission_classes = [IsAuthenticated,]
    queryset = models.Code_Work.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class CodeWorkCheckAPI(CodeWorkStatusAPI):
    serializer_class = serializers.CodeWorkCheckSerializer
    permission_classes = [CodeWorkPermission.CodeWorkExamRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.CodeWorkCheckAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Code_Work_CODEWORK_CHECK'])
    def update(self, request, *args, **kwargs):
        work = self.get_object()
        user = request.user
        if self.qrcode_check(request):
            pass
        else:
            return '', self.qrcode_response

        codework = models.Code_Work.objects.filter(uuid=kwargs['pk']).get()

        if codework.mission.group.users.filter(id=user.id).exists():
            response = super(CodeWorkCheckAPI,self).update(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                MISSION=work.mission.info,
                REASON=work.info,
                UUID=work.uuid,
            ), response
        else:
            return '', Response({'detail': u'您没有审核的权限'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CodeWorkRunAPI(CodeWorkStatusAPI):
    serializer_class = serializers.CodeWorkRunSerializer
    permission_classes = [CodeWorkPermission.CodeWorkRunRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.CodeWorkRunAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Code_Work_CODEWORK_RUN'])
    def update(self, request, *args, **kwargs):
        work = self.get_object()
        user = request.user
        if self.qrcode_check(request):
            pass
        else:
            return '', self.qrcode_response

        codework = models.Code_Work.objects.filter(uuid=kwargs['pk']).get()

        if codework.user.id == user.id:
            response = super(CodeWorkRunAPI,self).update(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                MISSION=work.mission.info,
                REASON=work.info,
                UUID=work.uuid,
            ), response
        else:
            return '', Response({'detail': u'您无法执行不是您发起的工单'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CodeWorkUploadFileAPI(WebTokenAuthentication, generics.UpdateAPIView):
    serializer_class = serializers.CodeWorkUploadFileSerializer
    queryset = models.Code_Work.objects.all()
    permission_classes = [CodeWorkPermission.CodeWorkUploadRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.CodeWorkUploadFileAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Code_Work_CODEWORK_UPLOAD'])
    def update(self, request, *args, **kwargs):
        work = self.get_object()
        user = request.user
        if self.qrcode_check(request):
            pass
        else:
            return '', self.qrcode_response

        codework = models.Code_Work.objects.filter(uuid=kwargs['pk']).get()

        if codework.user.id == user.id:
            response = super(CodeWorkUploadFileAPI,self).update(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                MISSION=work.mission.info,
                REASON=work.info,
                UUID=work.uuid,
            ), response
        else:
            return '', Response({'detail': u'您无法对不是您发起的工单上传文件'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CodeWorkResultsAPI(WebTokenAuthentication, generics.ListAPIView):
    queryset = models.Code_Work.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    permission_classes = [CodeWorkPermission.CodeWorkRunRequiredMixin, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status > 0:
            return Response({'detail': u'该工单处于正常状态'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'results': obj.push_mission.results}, status=status.HTTP_202_ACCEPTED)
