from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView,FormView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from models import Group,Host,Storage
from django.urls import reverse_lazy
import forms
from django.utils import timezone
from django.utils.translation import ugettext as _

class ManagerGroupListView(LoginRequiredMixin,FormView):
    template_name= 'group.html'
    form_class=forms.GroupForm

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)

class ManagerHostCreateView(LoginRequiredMixin,CreateView):
    model = Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'new_update_host.html'
    success_url = reverse_lazy('manager:host')

    def form_valid(self, form):
        self.host = host = form.save()
        host.create_by = self.request.user.username or 'Admin'
        host.date_created = timezone.now()
        host.save()
        return super(ManagerHostCreateView,self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context={
            'app':'Host',
            'action':'Create host',
        }
        kwargs.update(context)
        return super(ManagerHostCreateView,self).get_context_data(**kwargs)

    def get_success_url(self):
        return super(ManagerHostCreateView, self).get_success_url()



class ManagerHostUpdateView(LoginRequiredMixin,UpdateView):
    model = Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'new_update_host.html'
    success_url = reverse_lazy('manager:host')

    def get_context_data(self, **kwargs):
        context={
            'app':'Host',
            'action':'Update host',
        }
        kwargs.update(context)
        return super(ManagerHostUpdateView,self).get_context_data(**kwargs)

    def get_success_url(self):
        return super(ManagerHostUpdateView, self).get_success_url()


class ManagerGroupCreateView(LoginRequiredMixin,CreateView):
    model = Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupCreateView, self).get_context_data(**kwargs)
        hosts = Host.objects.all()
        context.update({'hosts':hosts})
        return context

    def form_valid(self, form):
        host_group = forms.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = Host.objects.filter(id__in=hosts_id_list)
        host_group.users.add(*hosts)
        host_group.save()
        return super(ManagerGroupCreateView,self).form_invalid(form)

    def get_success_url(self):
        return super(ManagerGroupCreateView,self).get_success_url()

class ManagerGroupUpdateView(LoginRequiredMixin,UpdateView):
    model = Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupUpdateView, self).get_context_data(**kwargs)
        hosts = Host.objects.all()
        group_hosts = [host.id for host in self.object.hosts.all()]
        context.update({
            'hosts':hosts,
            'group_hosts':group_hosts
        })
        return context

    def form_valid(self, form):
        host_group = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = Host.objects.filter(id__in=hosts_id_list)
        host_group.users.clear()
        host_group.users.add(*hosts)
        host_group.save()
        return super(ManagerGroupUpdateView,self).form_invalid(form)


class ManagerHostListView(LoginRequiredMixin,FormView):
    template_name='host.html'
    form_class = forms.HostForm

    def get_context_data(self, **kwargs):
        context= super(ManagerHostListView, self).get_context_data(**kwargs)
        context.update({'grouplist': Group.objects.all(),
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
    form_class=forms.StorageForm

    def get(self, request, *args, **kwargs):
        return super(ManagerStorageListView,self).get(request,*args,**kwargs)