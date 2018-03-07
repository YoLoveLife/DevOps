# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from rest_framework.pagination import PageNumberPagination
from manager.query import hostQuery
from manager.permission import group as GroupPermission
from manager.permission import host as HostPermission
from manager.permission import storage as StoragePermission
from timeline.decorator.manager import decorator_manager
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class ManagerGroupListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JSONWebTokenAuthentication,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset=models.Group.objects.all()
        return queryset

class ManagerGroupRemoveAPI(generics.DestroyAPIView):
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupDeleteRequiredMixin]

    def delete(self, request, *args, **kwargs):
        group = models.Group.objects.get(id=int(kwargs['pk']))
        if group.hosts.count() != 0:
            return Response({'detail': '该应用组下存在主机无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            group.delete()
            return Response({'detail': '删除成功'}, status=status.HTTP_201_CREATED)

class PagePa(PageNumberPagination):
    page_size_query_param='page_size'


class ManagerHostListByGroupAPI(generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = PagePa

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset = models.Host.objects.all()
            return queryset
        queryset=models.Group.objects.get(id=self.kwargs['pk']).hosts
        return queryset
    #
    # def paginate_queryset(self, queryset):


class ManagerHostRemoveAPI(generics.DestroyAPIView):
    serializer_class = serializers.HostSerializer
    permission_classes = [HostPermission.HostDeleteRequiredMixin]

    def delete(self, request, *args, **kwargs):
        host = models.Host.objects.get(id=int(kwargs['pk']))
        if host.storages.count() != 0:
            return Response({'detail': '该主机下存在存储无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif len(host.application_get()) !=0:
            return Response({'detail': '该主机下存在应用无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            models.Host.objects.get(id=int(kwargs['pk'])).delete()
            return Response({'detail': '删除成功'}, status=status.HTTP_201_CREATED)

class ManagerHostPasswordAPI(generics.ListAPIView):
    serializer_class = serializers.HostPasswordSerializer
    permission_classes = (HostPermission.HostPasswordRequiredMixin,)
    count = 0

    @decorator_manager(5, u'获取密码')
    def timeline_create(self,user):
        return user,None

    def get_queryset(self):#此处时由于RestFramework的permission会被调用两次 只能在这里使用装饰器
        if self.count == 0:
            self.count = self.count + 1
            self.timeline_create(self.request.user)
            host = models.Host.objects.filter(id=int(self.kwargs['pk']))
            return host

class ManagerStorageListAPI(generics.ListAPIView):
    module = models.Storage
    serializer_class = serializers.StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset=models.Storage.objects.all()
        return queryset

class ManagerStorageRemoveAPI(generics.DestroyAPIView):
    serializer_class = serializers.StorageSerializer
    permission_classes = [StoragePermission.StorageDeleteRequiredMixin]

    def delete(self, request, *args, **kwargs):
        models.Storage.objects.get(id=int(kwargs['pk'])).delete()
        return Response({'detail': '删除成功'}, status=status.HTTP_201_CREATED)


class ManagerStorageListByGroup(generics.ListAPIView):
    module = models.Storage
    serializer_class = serializers.StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            return {}
        #queryset=Storage.objects.filter(group_id=self.kwargs['pk'])
        queryset ={}
        return queryset

class ManagerSearchAPI(generics.ListAPIView):
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_list = self.request.query_params.dict()
        del query_list['order']
        del query_list['offset']
        del query_list['limit']
        if len(query_list) == 0:
            return {}
        else:
            return hostQuery(**query_list)


