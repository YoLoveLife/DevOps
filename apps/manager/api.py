# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from manager.query import hostQuery
class ManagerGroupListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.Group.objects.all()
        return queryset

class ManagerHostListByGroupAPI(generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset = models.Host.objects.all()
            return queryset
        queryset=models.Group.objects.get(id=self.kwargs['pk']).hosts
        return queryset

class ManagerStorageListAPI(generics.ListAPIView):
    module = models.Storage
    serializer_class = serializers.StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset=models.Storage.objects.all()
        return queryset


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