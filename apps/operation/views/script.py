from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView

class OperationScriptListView(LoginRequiredMixin,TemplateView):
    template_name='script.html'
    form_class = forms.ScriptForm

    def get_context_data(self, **kwargs):
        context= super(OperationScriptListView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(OperationScriptListView, self).get(request, *args, **kwargs)


class OperationScriptCreateView(LoginRequiredMixin,CreateView):
    template_name = 'new_update_script.html'
    form_class = forms.ScriptCreateUpdateForm
    success_url = reverse_lazy('operation:script')
    model = models.Script
    
    def form_valid(self, form):
        script_form = form.save()
        script_form.save()
        return super(OperationScriptCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OperationScriptCreateView,self).get_context_data(**kwargs)
        context.update({
            'app':'script'
        })
        return context

    def get_success_url(self):
        return self.success_url



'''
class ManagerStorageCreateView(LoginRequiredMixin,CreateView):
    template_name = 'new_update_storage.html'
    form_class = forms.StorageCreateUpdateForm
    success_url = reverse_lazy('manager:storage')
    model = models.Storage

    def form_valid(self, form):
        host_storage=form.save()
        hosts_id_list=self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_storage.hosts.add(*hosts)
        host_storage.save()
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


'''