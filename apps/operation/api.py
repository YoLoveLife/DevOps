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

        def delete(self, request, *args, **kwargs):
            # return self.destroy(self,request,args,kwargs)
            if models.Script.objects.get(id=int(kwargs['pk'])).scriptargs.filter(args_name=request.data['args_name']).exists():
                models.Script.objects.get(id=int(kwargs['pk'])).scriptargs.filter(args_name=request.data['args_name']).delete()
                return Response({'info':'删除成功'},status=status.HTTP_201_CREATED)
            else:
                return Response({'info':'参数在脚本中已不存在'},status=status.HTTP_406_NOT_ACCEPTABLE)



class PlaybookListAPI(generics.ListAPIView):
    serializer_class = serializers.PlaybookSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = models.PlayBook.objects.all()
        return queryset


class PlaybookTasksListAPI(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset={}
            return queryset
        queryset = models.PlayBook.objects.get(id=self.kwargs['pk']).tasks.order_by("sort")
        return queryset



class TaskCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        playbook = models.PlayBook.objects.get(id=int(kwargs['pk']))
        serializer.instance.playbook=playbook
        serializer.instance.sort = playbook.sort
        playbook.sort=playbook.sort+1
        playbook.save()
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TaskRemoveAPI(generics.DestroyAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
    # return self.destroy(self,request,args,kwargs)
        if models.PlayBook.objects.get(id=int(kwargs['pk'])).tasks.filter(sort=request.data['sort']).exists():
            models.PlayBook.objects.get(id=int(kwargs['pk'])).tasks.filter(sort=request.data['sort']).delete()
            return Response({'info': '删除成功'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'info': '任务在剧本中已不存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class TaskSortAPI(generics.UpdateAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        tasks = models.PlayBook.objects.get(id=int(kwargs['pk'])).tasks
        taskA = tasks.get(sort=int(request.data['parta']))
        taskB = tasks.get(sort=int(request.data['partb']))
        tempsort=taskA.sort
        taskA.sort=taskB.sort
        taskB.sort=tempsort
        taskA.save()
        taskB.save()
        return Response({'info': '转换成功'}, status=status.HTTP_201_CREATED)