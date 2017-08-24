# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class GroupListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.Group.objects.all()
        return queryset

class HostListByGroupAPI(generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset = models.Host.objects.all()
            return queryset
        queryset=models.Group.objects.get(id=self.kwargs['pk']).hosts
        return queryset


class StorageListAPI(generics.ListAPIView):
    module = models.Storage
    serializer_class = serializers.StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset=models.Storage.objects.all()
        return queryset


class StorageListByGroup(generics.ListAPIView):
    module = models.Storage
    serializer_class = serializers.StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            return {}
        #queryset=Storage.objects.filter(group_id=self.kwargs['pk'])
        queryset ={}
        return queryset

class SystemTypeAPI(generics.ListAPIView):
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)