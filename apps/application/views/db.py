# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from manager.models import Host
from timeline.models import History
from application.permission import db as DBPermission
from utils import aes
from .. import models, forms
from timeline.decorator.manager import decorator_manager

# Create your views here.
class ApplicationDBListView(LoginRequiredMixin,TemplateView):
    template_name= 'application/db/db.html'

    def get(self,request,*args, **kwargs):
        return super(ApplicationDBListView, self).get(request, *args, **kwargs)

class ApplicationDBDetailView(LoginRequiredMixin,DetailView):
    model = models.DB
    template_name = 'application/db/detail_db.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBDetailView,self).get_context_data(**kwargs)
        detail = self.object.dbdetail.get()
        context.update({
            'detail':detail
        })
        return context

class ApplicationDBCreateView(LoginRequiredMixin,DBPermission.DBAddRequiredMixin,CreateView):
    model = models.DB
    form_class = forms.DBCreateUpdateForm
    template_name = 'application/db/new_update_db.html'
    success_url = reverse_lazy('application:db')

    def form_valid(self, form):
        his=History(user=self.request.user,type=4,info="新增应用",status=0)
        his.save()

        db=form.save()
        service_ip = self.request.POST.get('service_ip')
        db.root_passwd =  aes.encrypt(db.root_passwd)
        if Host.objects.filter(service_ip = service_ip).count() == 1:
            host = Host.objects.filter(service_ip=service_ip).get()
            db.host = host
        else:
            pass
        dbdetail = models.DBDetail()
        dbdetail.db=db
        dbdetail.save()
        db.save()
        his.status=1
        his.save()
        return super(ApplicationDBCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBCreateView,self).get_context_data(**kwargs)
        context.update({
            'service_ip' : ''
        })
        return context

    def get_success_url(self):
        return self.success_url



class ApplicationDBUpdateView(LoginRequiredMixin,DBPermission.DBChangeRequiredMixin,UpdateView):
    model = models.DB
    form_class = forms.DBCreateUpdateForm
    template_name = 'application/db/new_update_db.html'
    success_url = reverse_lazy('application:db')

    @decorator_manager(4,u'修改DB应用')
    def form_valid(self, form):
        return self.request.user,super(ApplicationDBUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBUpdateView,self).get_context_data(**kwargs)
        context.update({
            'service_ip' : self.object.host.service_ip
        })
        return context

    def get_success_url(self):
        return self.success_url

class ApplicationDBAuthView(LoginRequiredMixin,DBPermission.DBAuthRequiredMixin,DetailView):
    model = models.DB
    template_name = 'application/db/auth_db.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationDBAuthView,self).get_context_data(**kwargs)
        return context