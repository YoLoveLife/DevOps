from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import CreateView,UpdateView

class ManagerStorageListView(LoginRequiredMixin,FormView):
    template_name = 'storage.html'
    form_class=forms.StorageForm

    def get(self, request, *args, **kwargs):
        return super(ManagerStorageListView,self).get(request,*args,**kwargs)


class ManagerStorageCreateView(LoginRequiredMixin,CreateView):
    model = models.Storage
    form_class = forms.StorageCreateUpdateForm
    template_name = 'new_update_storage.html'
    success_url = reverse_lazy('manager:storage')

    # def get_context_data(self, **kwargs):
    #     context = super(ManagerStorageCreateView, self).get_context_data(**kwargs)
    #     hosts = models.Host.objects.all()
    #     context.update({'hosts':hosts})
    #     return context

    def form_valid(self, form):
        host_storage = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_storage.hosts.add(*hosts)
        host_storage.save()
        return super(ManagerStorageCreateView,self).form_valid(form)

    def get_success_url(self):
        return self.success_url

class ManagerStorageUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Storage
    form_class = forms.StorageCreateUpdateForm
    template_name = 'new_update_storage.html'
    success_url = reverse_lazy('manager:storage')

    def get_context_data(self, **kwargs):
        context = super(ManagerStorageUpdateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        storage_hosts = [host.id for host in self.object.hosts.all()]
        context.update({
            'hosts':hosts,
            'storage_hosts':storage_hosts
        })
        return context

    def form_valid(self, form):
        host_storage = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_storage.hosts.clear()
        host_storage.hosts.add(*hosts)
        host_storage.save()
        return super(ManagerStorageUpdateView,self).form_valid(form)

    def get_success_url(self):
        return super(ManagerStorageUpdateView,self).get_success_url()