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
from forms import GroupForm,HostForm,StorageForm,HostCreateForm
from django.utils import timezone
from django.utils.translation import ugettext as _

class ManagerGroupListView(LoginRequiredMixin,FormView):
    template_name= 'group.html'
    form_class=GroupForm

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)

class ManagerHostCreateView(LoginRequiredMixin,CreateView):
    model = Host
    form_class = HostCreateForm
    template_name = '_new_host.html'
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
    form_class = HostCreateForm
    template_name = '_new_host.html'
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