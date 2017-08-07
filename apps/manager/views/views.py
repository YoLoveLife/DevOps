from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import FormView,TemplateView
from django.views.generic.edit import CreateView,UpdateView


class ManagerSearchListView(LoginRequiredMixin,TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        return super(ManagerSearchListView,self).get(request,*args,**kwargs)

class ManagerStorageListView(LoginRequiredMixin,FormView):
    template_name = 'storage.html'
    form_class=forms.StorageForm

    def get(self, request, *args, **kwargs):
        return super(ManagerStorageListView,self).get(request,*args,**kwargs)