# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from permission import jumper as JumperPermission
import forms as UtilForms
import models
from manager.models import System_Type
from timeline.decorator.manager import decorator_manager
from deveops.utils import aes
from django.http import HttpResponseRedirect

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


class UtilsView(LoginRequiredMixin,TemplateView):
    template_name = 'utils/utils.html'

    def get(self,request,*args, **kwargs):
        return super(UtilsView, self).get(request, *args, **kwargs)

class UtilsSystemTypeDeleteView(LoginRequiredMixin,DeleteView):
    model = System_Type
    template_name = 'utils/delete_utils_systype_modal.html'
    success_url = reverse_lazy('utils:other')

    def get_context_data(self, **kwargs):
        flag = 0
        detail = ""
        if self.object.sum_host > 0:
            detail = u'该系统类型存在关联主机无法删除 请确认无该类型的主机后在执行该操作'
        else:
            flag = 1

        context_data = super(UtilsSystemTypeDeleteView, self).get_context_data(**kwargs)
        context_data.update({
            'unable_delete': flag,
            'detail': detail,
        })
        return context_data

    @decorator_manager(0,u'删除操作系统')
    def delete(self, request, *args, **kwargs):
        return self.request.user,super(UtilsSystemTypeDeleteView,self).delete(request,*args,**kwargs)

class UtilsSystemTypeCreateView(LoginRequiredMixin,CreateView):
    model = System_Type
    template_name = 'utils/create_utils_systype_modal.html'
    success_url = reverse_lazy('utils:other')
    form_class = UtilForms.SystemTypeForm


    @decorator_manager(0,u'新增操作系统')
    def form_valid(self, form):
        #此处的form_valid包含一部分名字重复但是作为None值提交的
        return self.request.user,super(UtilsSystemTypeCreateView,self).form_valid(form=form)

    def get_success_url(self):
        return self.success_url