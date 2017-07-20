from collections import OrderedDict
from .models import Host,Group
from rest_framework import viewsets
from .serializers import HostSerializer,GroupSerializer
from rest_framework.views import Response
from rest_framework import generics


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    #def create(self, request, *args, **kwargs):


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

