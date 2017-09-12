# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from inventory.maker import Maker
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

class HostFlushAPI(generics.UpdateAPIView):
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        host = models.Host.objects.get(id=self.kwargs['pk'])
        maker = Maker()
        file=maker.inventory_maker([host])
        from yosible.run.playbook import Playbook
        from yosible.run.ansiblerun import Ansible
        from yosible.tasks.tasks import Task,Tasks

        pb = Playbook('ddr', 'no')
        b = Task(module="script", args="~/ddr.sh")
        s = Tasks()
        s.push_task(b)
        from callback.catch.basic import BasicResultCallback
        brc = BasicResultCallback()
        A = Ansible()
        pb.push_tasks(s)
        A.set_playbook(pb)
        A.set_callback(brc)
        A.run_playbook()


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