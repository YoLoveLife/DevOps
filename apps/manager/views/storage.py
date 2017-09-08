# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from timeline.models import History
from ..permission import storage as StoragePermission
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import CreateView,UpdateView

class ManagerStorageListView(LoginRequiredMixin,FormView):
    template_name = 'manager/storage.html'
    form_class=forms.StorageForm

    def get(self, request, *args, **kwargs):
        return super(ManagerStorageListView,self).get(request,*args,**kwargs)

class ManagerStorageCreateView(LoginRequiredMixin,StoragePermission.StorageAddRequiredMixin,CreateView):
    template_name = 'manager/new_update_storage.html'
    form_class = forms.StorageCreateUpdateForm
    success_url = reverse_lazy('manager:storage')
    model = models.Storage

    def form_valid(self, form):
        his=History(user=self.request.user,type=0,info="新增存储",status=0)
        his.save()

        host_storage=form.save()
        hosts_id_list=self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_storage.hosts.add(*hosts)
        host_storage.save()

        his.status=1
        his.save()
        return super(ManagerStorageCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerStorageCreateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        context.update({
            'hosts':hosts,'storage_hosts':{}
        })
        return context

    def get_success_url(self):
        return self.success_url

class ManagerStorageUpdateView(LoginRequiredMixin,StoragePermission.StorageChangeRequiredMixin,UpdateView):
    template_name = 'manager/new_update_storage.html'
    form_class = forms.StorageCreateUpdateForm
    success_url = reverse_lazy('manager:storage')
    model = models.Storage

    def form_valid(self, form):
        his=History(user=self.request.user,type=0,info="新增存储",status=0)
        his.save()

        host_storage=form.save()
        hosts_id_list=self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_storage.hosts.clear()
        host_storage.hosts.add(*hosts)
        host_storage.save()

        his.status=1
        his.save()
        return super(ManagerStorageUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerStorageUpdateView,self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        storage_hosts=[host.id for host in self.object.hosts.all()]
        context.update({

            'hosts':hosts,'storage_hosts':storage_hosts
        })
        return context