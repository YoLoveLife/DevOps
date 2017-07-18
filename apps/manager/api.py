from collections import OrderedDict
from .models import Host,Group
from rest_framework import viewsets
from .serializers import HostSerializer,GroupSerializer
from rest_framework.views import Response
tasks=OrderedDict()
class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    def create(self, request, *args, **kwargs):
        host=request.user.host
        Host.objects.create(host)
        task=tasks.get(host.name)
        tasks[host.name]=[]
        return Response({'msg':'Success','tasks':task},status=201)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

