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
from ..permission import codework as CodeWorkPermission
from deveops.api import WebTokenAuthentication

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
    permission_classes = [AllowAny, ]
    pagination_class = CodeWorkPagination
    filter_class = filter.CodeWorkFilter


class CodeWorkCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkSerializer
    permission_classes = [AllowAny,]


class CodeWorkStatusAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkStatusSerializer
    permission_classes = [AllowAny,]
    queryset = models.Code_Work.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class CodeWorkCheckAPI(CodeWorkStatusAPI):
    serializer_class = serializers.CodeWorkCheckSerializer
    # permission_classes = [CodeWorkPermission.CodeWorkExamRequiredMixin, IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        codework = models.Code_Work.objects.filter(uuid=kwargs['pk']).get()
        if codework.mission.group.users.filter(id=user.id).exists():
            return super(CodeWorkCheckAPI,self).update(request, *args, **kwargs)
        else:
            return Response({'detail': u'您没有审核的权限'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CodeWorkRunAPI(CodeWorkStatusAPI):
    serializer_class = serializers.CodeWorkRunSerializer
    # permission_classes = [CodeWorkPermission.CodeWorkExamRequiredMixin, IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        codework = models.Code_Work.objects.filter(uuid=kwargs['pk']).get()
        if codework.user.id == user.id:
            return super(CodeWorkRunAPI,self).update(request, *args, **kwargs)
        else:
            return Response({'detail':u'您无法执行不是您发起的工单'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CodeWorkUploadFileAPI(generics.UpdateAPIView):
    serializer_class = serializers.CodeWorkUploadFileSerializer
    queryset = models.Code_Work.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        user = request.user
        codework = models.Code_Work.objects.filter(uuid=kwargs['pk']).get()
        if codework.user.id == user.id:
            return super(CodeWorkUploadFileAPI,self).update(request, *args, **kwargs)
        else:
            return Response({'detail':u'您无法对不是您发起的工单上传文件'}, status=status.HTTP_406_NOT_ACCEPTABLE)