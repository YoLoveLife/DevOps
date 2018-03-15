# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from rest_framework.pagination import PageNumberPagination
from timeline.decorator.manager import decorator_manager
from permission import jumper as JumperPermission
from permission import systemtype as SystemTypePermission
from manager.models import System_Type,Sys_User

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

class UtilsSystemTypeListAPI(generics.ListAPIView):
    module = System_Type
    serializer_class = serializers.SystemTypeDetailSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = System_Type.objects.all()
        return queryset

class UtilsSystemTypeCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [SystemTypePermission.SystemTypeAddRequiredMixin]

    def create(self, request, *args, **kwargs):
        if System_Type.objects.filter(name=kwargs['name']).count() != 0:
            return Response({'detail': '该系统类型已存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            st = System_Type.objects.create(name=kwargs['name'])
            return Response({'detail': '创建系统类型成功'}, status=status.HTTP_201_CREATED)

class UtilsSystemTypeRemoveAPI(generics.DestroyAPIView):
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [SystemTypePermission.SystemTypeDeleteRequiredMixin]

    def delete(self, request, *args, **kwargs):
        st = models.System_Type.objects.get(id=int(kwargs['pk']))
        if st.hosts.count() != 0:
            return Response({'detail': '该系统类型下关联诸多主机'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            st.delete()
            return Response({'detail': '删除系统类型成功'}, status=status.HTTP_201_CREATED)

class UtilsUserListAPI(generics.ListAPIView):
    module = Sys_User
    serializer_class = serializers.SysUserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Sys_User.objects.all()
        return queryset