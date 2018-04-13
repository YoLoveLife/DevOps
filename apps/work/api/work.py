# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from ..permission import codework as CodeWorkPermission
from deveops.api import WebTokenAuthentication

__all__ = [

]


class CodeWorkPagination(PageNumberPagination):
    page_size = 10


class CodeWorkListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkSerializer
    queryset = models.Code_Work.objects.all().order_by('-id')
    permission_classes = [AllowAny, ]
    # permission_classes = [FilePermission.FileListRequiredMixin, IsAuthenticated]
    pagination_class = CodeWorkPagination


class CodeWorkCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkSerializer
    permission_classes = [AllowAny,]


class CodeWorkExamAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeStatusSerializer
    # permission_classes = [CodeWorkPermission.CodeWorkExamRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    queryset = models.Code_Work.objects.all()

    def update(self, request, *args, **kwargs):
        user = request.user
        codework = models.Code_Work.objects.filter(id=int(kwargs['pk'])).get()
        if codework.mission.group.users.filter(id=user.id).exists():
            return super(CodeWorkExamAPI,self).update(request, *args, **kwargs)
        else:
            return Response({'detail': u'您没有审核的权限'}, status=status.HTTP_406_NOT_ACCEPTABLE)

# class UtilsFileCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
#     module = models.FILE
#     serializer_class = serializers.FileSerializer
#     permission_classes = [AllowAny, ]
#     # permission_classes = [FilePermission.FileCreateRequiredMixin, IsAuthenticated]

class CodeWorkRunAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Code_Work
    serializer_class = serializers.CodeWorkStatusSerializer
    permission_classes = [AllowAny,]
    queryset = models.Code_Work.objects.all()


