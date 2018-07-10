# -*- coding:utf-8 -*-
from .. import models,filter
from .. import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import mission as MissionPermission
from deveops.api import WebTokenAuthentication
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

__all__ = [
    'MissionPagination', 'OpsMissionListAPI', 'OpsMissionListByPageAPI',
    'OpsMissionNeedFileCheckAPI', 'OpsMissionCreateAPI', 'OpsMissionDeleteAPI',
    'OpsMissionUpdateAPI', 'OpsMissionListByUserAPI', 'OpsMissionPlaybookAPI',
    'OpsMissionNeedFileCheckAPI',
]


class MissionPagination(PageNumberPagination):
    page_size = 10


class OpsMissionListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    permission_classes = [MissionPermission.MissionListRequiredMixin,IsAuthenticated]
    filter_class = filter.MissionFilter

    def get_queryset(self):
        pmn_groups = self.request.user.groups.all()
        groups = models.Group.objects.filter(pmn_groups__in=pmn_groups)
        queryset = models.Mission.objects.filter(group__in=groups)
        return queryset


class OpsMissionListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    permission_classes = [MissionPermission.MissionListRequiredMixin,IsAuthenticated]
    pagination_class = MissionPagination
    filter_class = filter.MissionFilter

    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Mission操作

    def get_queryset(self):
        user = self.request.user
        groups = models.Group.objects.filter(users=user)
        queryset = models.Mission.objects.filter(group_id__in=groups)
        return queryset


class OpsMissionListByUserAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    permission_classes = [MissionPermission.MissionListRequiredMixin,IsAuthenticated]
    filter_class = filter.MissionFilter

    def get_queryset(self):
        # 查询所有该用户所关联组的任务
        pmn_groups = self.request.user.groups.all()
        groups = models.Group.objects.filter(pmn_groups__in=pmn_groups)
        queryset = models.Mission.objects.filter(group__in=groups)
        return queryset


# :TODO 剧本展现
class OpsMissionPlaybookAPI(WebTokenAuthentication, APIView):
    module = models.Mission
    permission_classes = [IsAuthenticated,]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def get_object(self):
        return models.Mission.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        data = {'id':obj.id,'playbook':obj.playbook}
        return Response(data, status=status.HTTP_200_OK)


class OpsMissionCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    permission_classes = [MissionPermission.MissionCreateRequiredMixin, IsAuthenticated]

    # 校验用户QR-Code
    def create(self, request, *args, **kwargs):
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            request.data.pop('qrcode')
            return super(OpsMissionCreateAPI, self).create(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)



class OpsMissionUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    queryset = models.Mission.objects.all()
    permission_classes = [MissionPermission.MissionUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            return super(OpsMissionUpdateAPI, self).create(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class OpsMissionDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    queryset = models.Mission.objects.all()
    permission_classes = [MissionPermission.MissionDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            return super(OpsMissionDeleteAPI, self).create(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)

# :TODO 执行任务的文件列表传入
class OpsMissionNeedFileCheckAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Mission
    serializer_class = serializers.MissionNeedFileSerializer
    # permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    queryset = models.Mission.objects.all()
    permission_classes = [AllowAny,]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
