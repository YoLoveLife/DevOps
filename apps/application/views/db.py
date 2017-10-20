# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .. import models,forms
from timeline.models import History
from manager.models import Host
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,UpdateView
from django.views.generic.detail import DetailView
from ..permission import db as DBPermission
from django.urls import reverse_lazy
# Create your views here.
class ApplicationDBListView(LoginRequiredMixin,TemplateView):
    template_name= 'application/db.html'

    def get(self,request,*args, **kwargs):
        return super(ApplicationDBListView, self).get(request, *args, **kwargs)

class ApplicationDBDetailView(LoginRequiredMixin,DetailView):
    model = models.DB
    template_name = 'application/detail_mariadb.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBDetailView,self).get_context_data(**kwargs)
        detail = self.object.dbdetail.all()[0]
        context.update({
            'detail':detail
        })
        return context

class ApplicationDBCreateView(LoginRequiredMixin,DBPermission.DBAddRequiredMixin,CreateView):
    model = models.DB
    form_class = forms.DBCreateUpdateForm
    template_name = 'application/new_update_db.html'
    success_url = reverse_lazy('application:db')

    def form_valid(self, form):
        his=History(user=self.request.user,type=4,info="新增应用",status=0)
        his.save()

        db=form.save()
        service_ip = self.request.POST.get('service_ip')
        if Host.objects.filter(service_ip = service_ip).count() == 1:
            host = Host.objects.filter(service_ip=service_ip).get()
            db.host = host
        else:
            pass

        db.save()
        his.status=1
        his.save()
        return super(ApplicationDBCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBCreateView,self).get_context_data(**kwargs)
        context.update({
            'service_ip' : self.object.host.service_ip
        })
        return context

    def get_success_url(self):
        return self.success_url



class ApplicationDBUpdateView(LoginRequiredMixin,DBPermission.DBChangeRequiredMixin,UpdateView):
    model = models.DB
    form_class = forms.DBCreateUpdateForm
    template_name = 'application/new_update_db.html'
    success_url = reverse_lazy('application:db')

    def form_valid(self, form):
        his=History(user=self.request.user,type=4,info="修改应用",status=0)
        his.save()

        db=form.save()
        service_ip = self.request.POST.get('service_ip')
        if Host.objects.filter(service_ip = service_ip).count() == 1:
            host = Host.objects.filter(service_ip=service_ip).get()
            db.host = host
        else:
            pass

        db.save()
        his.status=1
        his.save()
        return super(ApplicationDBUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBUpdateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url