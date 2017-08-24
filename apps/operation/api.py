# -*- coding:utf-8 -*-
import models
import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
class ScriptListAPI(generics.ListAPIView):
    serializer_class = serializers.ScriptSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.Script.objects.all()
        return queryset

class ScriptArgsListAPI(generics.ListAPIView):
    serializer_class = serializers.ScriptArgsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset={}
            return queryset
        queryset = models.Script.objects.get(id=self.kwargs['pk']).scriptargs
        return queryset


class ScriptArgsCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.ScriptArgsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if models.Script.objects.get(id=int(kwargs['pk'])).scriptargs.filter(args_name=request.data['args_name']).exists():
            return Response({'info':'参数在该脚本中已经存在'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer.save()
        script = models.Script.objects.get(id=int(kwargs['pk']))
        serializer.instance.script=script
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ScriptRemoveArgsAPI(generics.DestroyAPIView):
        serializer_class = serializers.ScriptArgsSerializer
        permission_classes = [IsAuthenticated]
        queryset = models.ScriptArgs.objects.all()

        def delete(self, request, *args, **kwargs):
            # return self.destroy(self,request,args,kwargs)
            if models.Script.objects.get(id=int(kwargs['pk'])).scriptargs.filter(
                    args_name=request.data['args_name']).exists():
                models.Script.objects.get(id=int(kwargs['pk'])).scriptargs.filter(
                    args_name=request.data['args_name']).delete()
                return Response({'info':'删除成功'},status=status.HTTP_201_CREATED)
            else:
                return Response({'info':'参数在脚本中已不存在'},status=status.HTTP_406_NOT_ACCEPTABLE)


