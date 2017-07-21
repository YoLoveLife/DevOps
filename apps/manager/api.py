from collections import OrderedDict
from .models import Host,Group
from rest_framework import viewsets
from .serializers import HostSerializer,GroupSerializer
from rest_framework.views import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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
        queryset=Host.objects.filter(group_id=self.kwargs['pk'])
        return queryset