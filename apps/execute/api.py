# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from execute.service.catch.basic import BasicAnsibleService
from operation.models import PlayBook
from manager.models import Host
from service.catch.basic import BasicAnsibleService
class UpdateHostAPI(generics.ListAPIView):
    serializer_class = serializers.UpdateHostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Host.objects.filter(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        host = Host.objects.get(id=self.kwargs['pk'])
        playbook = PlayBook.objects.get(id=1)
        bas = BasicAnsibleService(hostlist=[host])
        bas.run(tasklist=playbook.tasks.all().order_by('-sort'),hostlist=[host])
        return super(UpdateHostAPI,self).get(request,*args,**kwargs)