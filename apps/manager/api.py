from collections import OrderedDict
from .models import Host,Group
from rest_framework import viewsets
from .serializers import HostSerializer,GroupSerializer
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
import json

class GroupListAPI(generics.ListAPIView):
    module = Group
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Group.objects.all()
        return queryset

class GroupCreateAPI(generics.CreateAPIView):
    module = Group
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        name=request.data['name']
        info=request.data['info']
        try:
            group=Group.objects.get(name=name)
            data={'success':False,'msg':'Group Already exist!'}
            return Response(data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            data = {'success':True,'msg': 'Create success!'}
            group=Group(name=name,info=info)
            group.save()
            return Response(data,status=status.HTTP_200_OK)




class HostListByGroupAPI(generics.ListAPIView):
    module = Host
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Host.objects.filter(group_id=self.kwargs['pk'])
        return queryset
