# -*- coding:utf-8 -*-
from .models import Host,Group,Storage
from .serializers import HostSerializer,GroupSerializer,StorageSerializer,SystemTypeSerializer
import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from .forms import HostForm,GroupForm,StorageForm
from rest_framework.permissions import IsAuthenticated
import query
class GroupListAPI(generics.ListAPIView):
    module = Group
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Group.objects.all()
        return queryset

class HostListByGroupAPI(generics.ListAPIView):
    module = Host
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset = Host.objects.all()
            return queryset
        queryset=Group.objects.get(id=self.kwargs['pk']).hosts
        return queryset


class StorageListAPI(generics.ListAPIView):
    module = Storage
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset=Storage.objects.all()
        return queryset


class StorageListByGroup(generics.ListAPIView):
    module = Storage
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            return {}
        #queryset=Storage.objects.filter(group_id=self.kwargs['pk'])
        queryset ={}
        return queryset

class SystemTypeAPI(generics.ListAPIView):
    serializer_class = SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)