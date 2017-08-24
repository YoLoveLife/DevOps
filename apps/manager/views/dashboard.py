from django.contrib.auth.mixins import LoginRequiredMixin
from .. import models
from django.views.generic import FormView,TemplateView
from .. import query
class ManagerDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'manager/dashboard.html'
    def get_context_data(self, **kwargs):
        context=super(ManagerDashboardView,self).get_context_data(**kwargs)
        numhost=models.Host.objects.count()
        numgroup=models.Group.objects.count()
        numstorage=models.Storage.objects.count()
        systemlist=query.systemtypeQuery()
        grouplist=query.groupQuery()
        context.update({
            'numhost':numhost,
            'numgroup':numgroup,
            'numstorage':numstorage,
            'systemlist':systemlist,
            'grouplist':grouplist,
        })
        return context

    def get(self,request,*args,**kwargs):
        return super(ManagerDashboardView,self).get(request,*args,**kwargs)


class ManagerSearchListView(LoginRequiredMixin,TemplateView):
    template_name = 'manager/search.html'

    def get(self, request, *args, **kwargs):
        return super(ManagerSearchListView,self).get(request,*args,**kwargs)


