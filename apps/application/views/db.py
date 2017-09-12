# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class ApplicationDBListView(LoginRequiredMixin,TemplateView):
    template_name= 'application/db.html'

    def get(self,request,*args, **kwargs):
        return super(ApplicationDBListView, self).get(request, *args, **kwargs)