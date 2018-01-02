# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from timeline.models import History
from ..permission import storage as StoragePermission
from django.urls import reverse_lazy
from django.views.generic import FormView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from timeline.decorator.manager import decorator_manager

class ManagerStorageListView(LoginRequiredMixin,TemplateView):
    template_name = 'manager/storage.html'

    def get(self, request, *args, **kwargs):
        return super(ManagerStorageListView,self).get(request,*args,**kwargs)

class ManagerStorageCreateView(LoginRequiredMixin,StoragePermission.StorageAddRequiredMixin,CreateView):
    template_name = 'manager/new_storage.html'
    form_class = forms.StorageCreateUpdateForm
    success_url = reverse_lazy('manager:storage')
    model = models.Storage

    @decorator_manager(0,u'新增存储')
    def form_valid(self, form):
        form.save_hosts_new()
        return self.request.user,super(ManagerStorageCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerStorageCreateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url

class ManagerStorageUpdateView(LoginRequiredMixin,StoragePermission.StorageChangeRequiredMixin,UpdateView):
    template_name = 'manager/update_storage.html'
    form_class = forms.StorageCreateUpdateForm
    success_url = reverse_lazy('manager:storage')
    model = models.Storage

    @decorator_manager(0,u'更新存储')
    def form_valid(self, form):
        form.save_hosts_update()
        return self.request.user,super(ManagerStorageUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerStorageUpdateView,self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        storage_hosts=[host.id for host in self.object.hosts.all()]
        context.update({
            'hosts':hosts,'storage_hosts':storage_hosts
        })
        return context