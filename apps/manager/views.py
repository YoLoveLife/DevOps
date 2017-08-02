from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from models import Group,Host,Storage
from forms import GroupForm,HostForm,StorageForm

class ManagerGroupListView(LoginRequiredMixin,FormView):
    template_name= 'group.html'
    form_class=GroupForm

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)

class ManagerHostNew(LoginRequiredMixin,FormView):
    template_name = '_new_host.html'
    form_class=GroupForm

    def get_context_data(self, **kwargs):
        context = super(ManagerHostNew, self).get_context_data(**kwargs)
        if self.kwargs['pk'] == '0' :
            context.update({'host':''})
        else:
            host=Host.objects.get(id=self.kwargs['pk'])
            group=Group.objects.all()
            storage=Storage.objects.all().filter(group_id=host.group_id)
            context.update({'host':host,'group_list':group,'storage':storage})
        return context


    def get(self, request, *args, **kwargs):
        return super(ManagerHostNew, self).get(request, *args, **kwargs)


class ManagerHostListView(LoginRequiredMixin,FormView):
    template_name='host.html'
    form_class = HostForm

    def get_context_data(self, **kwargs):
        context= super(ManagerHostListView, self).get_context_data(**kwargs)
        grouplist = Group.objects.all()
        context.update({'grouplist': grouplist,
                        })
        return context

    def get(self,request,*args, **kwargs):
        return super(ManagerHostListView, self).get(request, *args, **kwargs)


class ManagerSearchListView(LoginRequiredMixin,TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        return super(ManagerSearchListView,self).get(request,*args,**kwargs)

class ManagerStorageListView(LoginRequiredMixin,FormView):
    template_name = 'storage.html'
    form_class=StorageForm

    def get(self, request, *args, **kwargs):
        return super(ManagerStorageListView,self).get(request,*args,**kwargs)