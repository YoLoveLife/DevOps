# -*- coding:utf-8 -*-
from .models import Host,Group,Storage
from .serializers import HostSerializer,GroupSerializer,StorageSerializer
from rest_framework.views import Response,status
from rest_framework import generics
from .forms import HostForm,GroupForm,StorageForm
from rest_framework.permissions import IsAuthenticated

class GroupListAPI(generics.ListAPIView):
    module = Group
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Group.objects.all()
        return queryset

class GroupCreateAPI(generics.UpdateAPIView):
    module = Group
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        gf=GroupForm(request.POST)
        if gf.is_valid():
            data=gf.clean()
            if data['success']==False:
                return Response(data,status=status.HTTP_200_OK)
            else :
                if data['data']['id'] == '#New':
                    group = Group(name=data['data']['name'], info=data['data']['info'])
                    group.save()
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    group = Group(id=data['data']['id'])
                    group.name = data['data']['name']
                    group.info = data['data']['info']
                    group.save()
                    return Response(data, status=status.HTTP_200_OK)
        else:
            data={'success':False,'msg':'存在字段为空'}
            return Response(data,status=status.HTTP_200_OK)

class HostListByGroupAPI(generics.ListAPIView):
    module = Host
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            return {}
        queryset=Host.objects.filter(group_id=self.kwargs['pk'])
        return queryset


class HostCreateAPI(generics.CreateAPIView):
    module = Host
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        hf=HostForm(request.POST)

        if hf.is_valid():#数据校验
            data=hf.clean()
            if data['success']==False:
                return Response(data,status=status.HTTP_200_OK)
            else:
                if data['data']['id'] == '#New':
                    host=hostDataClean(data['data'],1)
                else:
                    hostDataClean(data['data'],2)
            return Response(data, status=status.HTTP_200_OK)
        else:
            data={'success':False,'msg':'存在字段错误'}
            return Response(data,status=status.HTTP_200_OK)

def hostDataClean(data,type):
    if type==1 : #ADD
        host=Host(group_id=data['group'],systemtype=data['systemtype'],
                  manage_ip=data['manage_ip'],service_ip=data['service_ip'],
                  outer_ip=data['outer_ip'],server_position=data['server_position'],
                  hostname=data['hostname'],normal_user=data['normal_user'],
                  sshpasswd=data['sshpasswd'],sshport=data['sshport'],
                  coreness=data['coreness'],memory=data['memory'],
                  root_disk=data['root_disk'],info=data['info'])
        host.save()
        return
    elif type==2 :#EDIT
        host=Host.objects.filter(id=data['id'])
        host.update(group_id=data['group'],systemtype=data['systemtype'],
                  manage_ip=data['manage_ip'],service_ip=data['service_ip'],
                  outer_ip=data['outer_ip'],server_position=data['server_position'],
                  hostname=data['hostname'],normal_user=data['normal_user'],
                  sshpasswd=data['sshpasswd'],sshport=data['sshport'],
                  coreness=data['coreness'],memory=data['memory'],
                  root_disk=data['root_disk'],info=data['info'])
        return


class StorageListAPI(generics.ListAPIView):
    module = Storage
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset=Storage.objects.all()
        return queryset

class StorageCreateAPI(generics.CreateAPIView):
    module = Storage
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sf=StorageForm(request.POST)
        if sf.is_valid():
            data=sf.clean()
            if data['success']==False:
                return Response(data,status=status.HTTP_200_OK)
            else:
                if data['data']['id'] == '#New':
                    storage=Storage(disk_size=data['data']['disk_size'],
                                   disk_path=data['data']['disk_path'],
                                   info=data['data']['info'])
                    storage.save()
                else:
                    storage=Storage.objects.filter(id=data['data']['id'])
                    storage.update(disk_size=data['data']['disk_size'],
                                   disk_path=data['data']['disk_path'],
                                   info=data['data']['info'])
            return Response(data,status=status.HTTP_200_OK)
        else:
            data={'success':False,'msg':'存在字段错误'}
            return Response(data,status=status.HTTP_200_OK)


class StorageListByGroup(generics.ListAPIView):
    module = Storage
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            return {}
        queryset=Storage.objects.filter(group_id=self.kwargs['pk'])
        return queryset

