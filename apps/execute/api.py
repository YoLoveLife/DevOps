# -*- coding:utf-8 -*-
from application.models import DB
from execute.callback import ResultCallback
# from execute.service.catch.db import DBAnsibleService
from manager.models import Host
from operation.models import PlayBook
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

import serializers
from execute.ansible.runner import YoRunner

class UpdateHostAPI(generics.ListAPIView):
    serializer_class = serializers.UpdateHostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Host.objects.filter(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        # host = Host.objects.get(id=self.kwargs['pk'])
        # playbook = PlayBook.objects.get(id = 1)
        # bas = BasicAnsibleService(hostlist=[host])
        # bas.run(tasklist=playbook.tasks.all().order_by('-sort'))
        hosts = Host.objects.all()
        runner = YoRunner(hosts=hosts,extra_vars={'ddr':'ls','zzc':'hostname'})
        runner.set_callback(ResultCallback())
        playbook = PlayBook.objects.all()[0]
        ret = runner.run(playbook.tasks.all())
        return super(UpdateHostAPI,self).get(request,*args,**kwargs)

class CatchDBStatusAPI(generics.ListAPIView):
    serializer_class = serializers.CatchDBStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DB.objects.filter(id=self.kwargs['pk'])[0].dbdetail.all()

    def get(self, request, *args, **kwargs):
        db = DB.objects.filter(id=self.kwargs['pk'])[0]
        # dbdetail = db.dbdetail.all()[0]
        playbook = PlayBook.objects.get(id = 3)
        bas = DBAnsibleService(hostlist = [db.host] )
        bas.run(tasklist=playbook.tasks.all().order_by('-sort'),db=db)
        return super(CatchDBStatusAPI,self).get(request, *args, **kwargs)