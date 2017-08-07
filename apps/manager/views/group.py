from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import CreateView,UpdateView

class ManagerGroupListView(LoginRequiredMixin,FormView):
    template_name= 'group.html'
    form_class=forms.GroupForm

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)


class ManagerGroupCreateView(LoginRequiredMixin,CreateView):
    model = models.Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupCreateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        context.update({'hosts':hosts})
        return context

    def form_valid(self, form):
        host_group = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_group.hosts.add(*hosts)
        host_group.save()
        return super(ManagerGroupCreateView,self).form_invalid(form)

    def get_success_url(self):
        return super(ManagerGroupCreateView,self).get_success_url()

class ManagerGroupUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'new_update_group.html'
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
        host_group = form.save()
        hosts_id_list = self.request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)
        host_group.hosts.clear()
        host_group.hosts.add(*hosts)
        host_group.save()
        return super(ManagerGroupUpdateView,self).form_invalid(form)

    def get_success_url(self):
        return super(ManagerGroupCreateView,self).get_success_url()