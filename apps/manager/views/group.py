# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms,models
from timeline.models import History
from ..permission import group as GroupPermission
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required

class ManagerGroupListView(LoginRequiredMixin,FormView):
    template_name= 'manager/group.html'
    form_class=forms.GroupForm

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)

class ManagerGroupCreateView(LoginRequiredMixin,GroupPermission.GroupAddRequiredMixin,CreateView):
    model = models.Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'manager/new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupCreateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        context.update({'hosts':hosts})
        return context

    def form_valid(self, form):
        his=History(user=self.request.user,type=0,info="创建新的应用组",status=0)
        his.save()

        host_group = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_group.hosts.add(*hosts)
        host_group.save()

        his.status=1
        his.save()
        return super(ManagerGroupCreateView,self).form_valid(form)

    def get_success_url(self):
         return self.success_url

class ManagerGroupUpdateView(LoginRequiredMixin,GroupPermission.GroupChangeRequiredMixin,UpdateView):
    model = models.Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'manager/new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupUpdateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        group_hosts = [host.id for host in self.object.hosts.all()]
        context.update({
            'hosts':hosts,
            'group_hosts':group_hosts
        })
        return context

    def form_valid(self, form):
        his=History(user=self.request.user,type=0,info="修改应用组",status=0)
        his.save()

        host_group = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_group.hosts.clear()
        host_group.hosts.add(*hosts)
        host_group.save()

        his.status=1
        his.save()
        return super(ManagerGroupUpdateView,self).form_valid(form)

    def get_success_url(self):
        return self.success_url

class ManagerGroupDetailView(LoginRequiredMixin,DetailView):
    model = models.Group
    template_name = 'manager/detail_group.html'

    def get_context_data(self, **kwargs):
        context=super(ManagerGroupDetailView,self).get_context_data(**kwargs)
        group=self.object
        hosts=self.object.hosts.all()
        context.update({
            'group':group,
            'hosts':hosts,
        })
        return context