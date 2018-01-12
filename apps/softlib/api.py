# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from manager.query import hostQuery
from manager.permission import group as GroupPermission
from manager.permission import host as HostPermission
from manager.permission import storage as StoragePermission

class SoftlibListAPI(generics.ListAPIView):
    module = models.Softlib
    serializer_class = serializers.SoftlibSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = models.Softlib.objects.all()
        return queryset