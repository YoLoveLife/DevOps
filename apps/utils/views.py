# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,UpdateView
from django.urls import reverse_lazy
from permission import jumper as JumperPermission
import forms as UtilForms
import models
from timeline.decorator.manager import decorator_manager
from deveops.utils import aes


class UtilsJumperView(LoginRequiredMixin,TemplateView):
    template_name = 'utils/jumper.html'

    def get(self,request,*args, **kwargs):
        return super(UtilsJumperView, self).get(request, *args, **kwargs)


class UtilsJumperCreateView(LoginRequiredMixin,JumperPermission.JumperAddRequiredMixin,CreateView):
    model = models.Jumper
    template_name = 'utils/new_update_jumper.html'
    form_class = UtilForms.JumperCreateForm
    success_url = reverse_lazy('utils:jumper')

    @decorator_manager(0,u'创建跳板机')
    def form_valid(self, form):
        return self.request.user,super(UtilsJumperCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url


class UtilsJumperUpdateView(LoginRequiredMixin,JumperPermission.JumperChangeRequiredMixin,UpdateView):
    model = models.Jumper
    template_name = 'utils/new_update_jumper.html'
    form_class = UtilForms.JumperUpdateForm
    success_url = reverse_lazy('utils:jumper')

    def get_form(self, form_class=None):
        form = super(UtilsJumperUpdateView,self).get_form(form_class)
        form.initial['sshpasswd'] = aes.decrypt(form.initial['sshpasswd'])
        return form

    @decorator_manager(0,u'修改跳板机')
    def form_valid(self, form):
        return self.request.user,super(UtilsJumperUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url