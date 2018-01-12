# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models
from permission import softlib as SoftlibPermission
from django.urls import reverse_lazy
from django.views.generic import FormView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from timeline.decorator.manager import decorator_manager

class SoftlibListView(LoginRequiredMixin,TemplateView):
    template_name = 'softlib/softlib.html'

    def get(self, request, *args, **kwargs):
        return super(SoftlibListView,self).get(request,*args,**kwargs)

class SoftlibCreateView(LoginRequiredMixin,SoftlibPermission.SoftlibAddRequiredMixin,CreateView):
    template_name = 'softlib/new_storage.html'
    form_class = forms.SoftlibCreateUpdateForm
    success_url = reverse_lazy('softlib:storage')
    model = models.Softlib

    @decorator_manager(0,u'新增存储')
    def form_valid(self, form):
        return self.request.user,super(SoftlibCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SoftlibCreateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url

class SoftlibUpdateView(LoginRequiredMixin,SoftlibPermission.SoftlibChangeRequiredMixin,UpdateView):
    template_name = 'softlib/update_storage.html'
    form_class = forms.SoftlibCreateUpdateForm
    success_url = reverse_lazy('softlib:')
    model = models.Softlib

    @decorator_manager(0,u'更新存储')
    def form_valid(self, form):
        return self.request.user,super(SoftlibUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SoftlibUpdateView,self).get_context_data(**kwargs)
        return context