# -*- coding:utf-8 -*-
# from application.models import DB
from manager.models import Host
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from execute.service.base import PingOnlineService
import serializers


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
        PingOnlineService()
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