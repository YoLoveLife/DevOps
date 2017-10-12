# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .. import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

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