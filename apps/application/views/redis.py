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

# class ApplicationDBDetailView(LoginRequiredMixin,DetailView):
#     model = models.DB
#     template_name = 'application/db/detail_db.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ApplicationDBDetailView,self).get_context_data(**kwargs)
#         detail = self.object.dbdetail.get()
#         context.update({
#             'detail':detail
#         })
#         return context
#
class ApplicationRedisCreateView(LoginRequiredMixin,RedisPermission.RedisAddRequiredMixin,CreateView):
    model = models.Redis
    form_class = forms.RedisCreateUpdateForm
    template_name = 'application/redis/new_update_redis.html'
    success_url = reverse_lazy('application:redis')

    @decorator_manager(4,u'新增Redis应用')
    def form_valid(self, form):
        redis = form.save()
        service_ip = self.request.POST.get('service_ip')
        redis.root_passwd =  aes.encrypt(redis.root_passwd)
        return self.request.user,super(ApplicationRedisCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationRedisCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url
#
#
#
# class ApplicationDBUpdateView(LoginRequiredMixin,RedisPermission.RedisChangeRequiredMixin,UpdateView):
#     model = models.DB
#     form_class = forms.DBCreateUpdateForm
#     template_name = 'application/db/new_update_db.html'
#     success_url = reverse_lazy('application:db')
#
#     def form_valid(self, form):
#         his=History(user=self.request.user,type=4,info="修改应用",status=0)
#         his.save()
#
#         db=form.save()
#         service_ip = self.request.POST.get('service_ip')
#         db.root_passwd =  aes.encrypt(db.root_passwd)
#         if Host.objects.filter(service_ip = service_ip).count() == 1:
#             host = Host.objects.filter(service_ip=service_ip).get()
#             db.host = host
#         else:
#             pass
#
#         db.save()
#         his.status=1
#         his.save()
#         return super(ApplicationDBUpdateView,self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(ApplicationDBUpdateView,self).get_context_data(**kwargs)
#         context.update({
#             'service_ip' : self.object.host.service_ip
#         })
#         return context
#
#     def get_success_url(self):
#         return self.success_url