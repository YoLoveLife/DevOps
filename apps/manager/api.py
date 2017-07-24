# -*- coding:utf-8 -*-
from .models import Host,Group
from .serializers import HostSerializer,GroupSerializer
from rest_framework.views import Response,status
from rest_framework import generics
from .forms import HostForm,GroupForm
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
        name=request.data['name']
        info=request.data['info']
        gf=GroupForm(request.POST)
        if gf.is_valid():
            data=gf.clean()
            if data['success']==True:
                group=Group(name=data['name'][0],info=data['info'][0])
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
        queryset=Host.objects.filter(group_id=self.kwargs['pk'])
        return queryset


class HostCreateAPI(generics.CreateAPIView):
    module = Host
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        hf=HostForm(request.POST)
        data={}
        #postdata=request.data
        #if
        #host=Host()

        return Response(data,status=status.HTTP_200_OK)