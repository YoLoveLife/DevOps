# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from manager.models import Host
from timeline.models import History
from application.permission import redis as RedisPermission
from timeline.decorator.manager import decorator_manager
from deveops.utils import aes
from .. import models, forms


# Create your views here.
class ApplicationRedisListView(LoginRequiredMixin,TemplateView):
    template_name= 'application/redis/redis.html'

    def get(self,request,*args, **kwargs):
        return super(ApplicationRedisListView, self).get(request, *args, **kwargs)

class ApplicationRedisCreateView(LoginRequiredMixin,RedisPermission.RedisAddRequiredMixin,CreateView):
    model = models.Redis
    form_class = forms.RedisCreateUpdateForm
    template_name = 'application/redis/new_update_redis.html'
    success_url = reverse_lazy('application:redis')

    @decorator_manager(4,u'新增Redis应用')
    def form_valid(self, form):
        return self.request.user,super(ApplicationRedisCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationRedisCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url

class ApplicationRedisUpdateView(LoginRequiredMixin,RedisPermission.RedisChangeRequiredMixin,UpdateView):
    model = models.Redis
    form_class = forms.RedisCreateUpdateForm
    template_name = 'application/redis/new_update_redis.html'
    success_url = reverse_lazy('application:redis')

    def get_form(self, form_class=None):
        form = super(ApplicationRedisUpdateView, self).get_form(form_class)
        form.initial['redis_passwd'] = aes.decrypt(form.instance.redis_passwd)
        return form

    @decorator_manager(4,u'修改Redis应用')
    def form_valid(self, form):
        return self.request.user,super(ApplicationRedisUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationRedisUpdateView,self).get_context_data(**kwargs)
        context.update({
            'service_ip' : self.object.host.service_ip
        })
        return context

    def get_success_url(self):
        return self.success_url