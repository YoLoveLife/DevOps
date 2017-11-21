# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .. import forms
from .. import models
from ..permission import host as HostPermission
from deveops.utils import aes
from timeline.decorator.manager import decorator_manager

class ManagerHostListView(LoginRequiredMixin,TemplateView):
    template_name='manager/host.html'

    def get_context_data(self, **kwargs):
        context= super(ManagerHostListView, self).get_context_data(**kwargs)
        context.update({'grouplist': models.Group.objects.all(),
                        })
        return context

    def get(self,request,*args, **kwargs):
        return super(ManagerHostListView, self).get(request, *args, **kwargs)

class ManagerHostCreateView(LoginRequiredMixin,HostPermission.HostAddRequiredMixin,CreateView):
    model = models.Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'manager/new_update_host.html'
    success_url = reverse_lazy('manager:host')

    @decorator_manager(0,u'新增应用主机')
    def form_valid(self, form):
        form.before_save(request=self.request,commit=True)
        # super(ManagerHostCreateView,self).form_valid(form)
        return self.request.user,super(ManagerHostCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerHostCreateView,self).get_context_data(**kwargs)
        groups = models.Group.objects.all()
        storages = models.Storage.objects.all()
        context.update({
            'groups':groups,
            'groups_host':{},
            'storages':storages,
            'storages_host':{}
        })
        return context

    def get_success_url(self):
        return self.success_url


class ManagerHostUpdateView(LoginRequiredMixin,HostPermission.HostChangeRequiredMixin,UpdateView):
    model = models.Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'manager/new_update_host.html'
    success_url = reverse_lazy('manager:host')

    @decorator_manager(0,u'修改应用主机')
    def form_valid(self, form):
        form.before_save(request=self.request,commit=True)
        return self.request.user,super(ManagerHostUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super(ManagerHostUpdateView,self).get_context_data(**kwargs)
        groups = models.Group.objects.all()
        groups_host = [group.id for group in self.object.groups.all()]

        storages = models.Storage.objects.all()
        storages_host = [storage.id for storage in self.object.storages.all()]
        context.update({
            'groups':groups,
            'groups_host':groups_host,
            'storages':storages,
            'storages_host':storages_host
        })
        return context

    def get_success_url(self):
        return self.success_url

class ManagerHostDetailView(LoginRequiredMixin,DetailView):
    model = models.Host
    template_name = 'manager/detail_host.html'

    def get_context_data(self, **kwargs):
        context=super(ManagerHostDetailView,self).get_context_data(**kwargs)
        groups=self.object.groups.all()
        storages=self.object.storages.all()
        softlibs = self.object.application_get()
        manage_user = self.object.manage_user_get()
        context.update({
            'groups':groups,
            'storages':storages,
            'softlibs':softlibs,
            'manage_user':manage_user,
        })
        return context