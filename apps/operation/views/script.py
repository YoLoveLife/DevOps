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


# class OperationScriptCreateView(LoginRequiredMixin,CreateView):
#     template_name = 'new_update_script.html'
#     form_class = forms.ScriptCreateUpdateForm
#     success_url = reverse_lazy('operation:script')
#     model = models.Script
#
#     def form_valid(self, form):
#         script_form = form.save()
#         script_form.save()
#         return super(OperationScriptCreateView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(OperationScriptCreateView,self).get_context_data(**kwargs)
#         context.update({
#             'app':'script'
#         })
#         return context
#
#     def get_success_url(self):
#         return self.success_url

class OperationScriptUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'new_update_script.html'
    form_class = forms.ScriptCreateUpdateForm
    success_url = reverse_lazy('operation:script')
    model = models.Script
    id = 0
    def get_object(self, queryset=None):
        if self.kwargs['pk'] == '0':
            script=models.Script.objects.create()
            self.id=script.id
            return script
        else:
            id=self.kwargs['pk']
            return models.Script.objects.get(id = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(OperationScriptUpdateView,self).get_context_data(**kwargs)

        context.update({
            'id':self.id
        })
        return context



'''
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
'''