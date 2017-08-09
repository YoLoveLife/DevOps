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
        self.host = host = form.save()
        host.save()
        return super(ManagerHostCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerHostCreateView,self).get_context_data(**kwargs)
        context.update({
            'app':'Host',
            'action':'Create host',
        })
        return context

    def get_success_url(self):
        return self.success_url



class ManagerHostUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Host
    form_class = forms.HostCreateUpdateForm
    template_name = 'new_update_host.html'
    success_url = reverse_lazy('manager:host')

    def get_context_data(self, **kwargs):
        context=super(ManagerHostUpdateView,self).get_context_data(**kwargs)
        context.update({
            'app':'Host',
            'action':'Update host',
        })
        return context

    def get_success_url(self):
        return self.success_url

class ManagerHostDetailVIew(LoginRequiredMixin,DetailView):
    model = models.Host
    template_name = 'detail_host.html'

    def get_context_data(self, **kwargs):
        context=super(ManagerHostDetailVIew,self).get_context_data(**kwargs)
        context.update({
            'groups':{}
        })

        return context