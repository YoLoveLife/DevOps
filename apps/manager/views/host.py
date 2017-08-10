from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView

class ManagerHostListView(LoginRequiredMixin,FormView):
    template_name='host.html'
    form_class = forms.HostForm

    def get_context_data(self, **kwargs):
        context= super(ManagerHostListView, self).get_context_data(**kwargs)
        context.update({'grouplist': models.Group.objects.all(),
                        })
        return context

    def get(self,request,*args, **kwargs):
        return super(ManagerHostListView, self).get(request, *args, **kwargs)

class ManagerHostCreateView(LoginRequiredMixin,CreateView):
    model = models.Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'new_update_host.html'
    success_url = reverse_lazy('manager:host')

    def form_valid(self, form):
        host_storage_group=form.save()
        hosts_id_list=self.request.POST.getlist('groups',[])
        storages_id_list=self.request.POST.getlist('storages',[])

        groups = models.Group.objects.filter(id__in=hosts_id_list)
        storages = models.Storage.objects.filter(id__in=storages_id_list)

        host_storage_group.groups.add(*groups)
        host_storage_group.storages.add(*storages)
        host_storage_group.save()

        return super(ManagerHostCreateView,self).form_valid(form)

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



class ManagerHostUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'new_update_host.html'
    success_url = reverse_lazy('manager:host')

    def form_valid(self, form):
        host_storage_group=form.save()
        hosts_id_list=self.request.POST.getlist('groups',[])
        storages_id_list=self.request.POST.getlist('storages',[])

        groups = models.Group.objects.filter(id__in=hosts_id_list)
        storages = models.Storage.objects.filter(id__in=storages_id_list)

        host_storage_group.groups.add(*groups)
        host_storage_group.storages.add(*storages)
        host_storage_group.save()
        return super(ManagerHostUpdateView, self).form_valid(form)

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

class ManagerHostDetailVIew(LoginRequiredMixin,DetailView):
    model = models.Host
    template_name = 'detail_host.html'

    def get_context_data(self, **kwargs):
        context=super(ManagerHostDetailVIew,self).get_context_data(**kwargs)
        groups=self.object.groups.all()
        storages=self.object.storages.all()
        host=self.object
        context.update({
            'groups':groups,
            'storages':storages,
            'host':host
        })
        return context