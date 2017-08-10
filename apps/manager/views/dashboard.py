from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import FormView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from ..utils import systemtype2json
class ManagerDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        context=super(ManagerDashboardView,self).get_context_data(**kwargs)
        numhost=models.Host.objects.count()
        numgroup=models.Group.objects.count()
        numstorage=models.Storage.objects.count()
        list=systemtype2json()
        context.update({
            'numhost':numhost,
            'numgroup':numgroup,
            'numstorage':numstorage,
            'systemtype':list,
        })
        return context

    def get(self,request,*args,**kwargs):
        return super(ManagerDashboardView,self).get(request,*args,**kwargs)


class ManagerSearchListView(LoginRequiredMixin,TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        return super(ManagerSearchListView,self).get(request,*args,**kwargs)


