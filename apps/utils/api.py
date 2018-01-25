# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from rest_framework.pagination import PageNumberPagination
from timeline.decorator.manager import decorator_manager
from permission import jumper as JumperPermission

class UtilsJumperListAPI(generics.ListAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = models.Jumper.objects.all()
        return queryset


class UtilsJumperRemoveAPI(generics.DestroyAPIView):
    serializer_class = serializers.JumperSerializer
    permission_classes = [JumperPermission.JumperDeleteRequiredMixin]

    def delete(self, request, *args, **kwargs):
        jumper = models.Jumper.objects.get(id=int(kwargs['pk']))
        if jumper.groups.count() != 0:
            return Response({'detail': '该跳板机下存在应用组无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            jumper.delete()
            return Response({'detail': '删除成功'}, status=status.HTTP_201_CREATED)
