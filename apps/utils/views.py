# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,UpdateView
from django.urls import reverse_lazy
import forms as UtilForms
import models

class UtilsJumperView(LoginRequiredMixin,TemplateView):
    template_name= 'utils/jumper.html'

    def get(self,request,*args, **kwargs):
        return super(UtilsJumperView, self).get(request, *args, **kwargs)


class UtilsJumperCreateModalView(LoginRequiredMixin,CreateView):
    model = models.Jumper
    template_name = 'utils/jumper_modal.html'
    form_class = UtilForms.JumperCreateForm
    success_url = reverse_lazy('utils:jumper')

    # @decorator_manager(0,u'修改应用主机')
    def form_valid(self, form):
        return self.request.user,super(UtilsJumperCreateModalView, self).form_valid(form)

class UtilsJumperUpdateModalView(LoginRequiredMixin,UpdateView):
    model = models.Jumper
    template_name = 'utils/jumper_modal.html'
    form_class = UtilForms.JumperUpdateForm
    success_url = reverse_lazy('utils:jumper')
    # @decorator_manager(0,u'修改应用主机')
    # def get_queryset(self):
    #
    def get_form(self, form_class=None):
        form = super(UtilsJumperUpdateModalView,self).get_form(form_class)
        return form

    def form_valid(self, form):
        return self.request.user,super(UtilsJumperUpdateModalView, self).form_valid(form)