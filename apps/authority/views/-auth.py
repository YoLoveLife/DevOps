# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.
class AuthorityGroupView(LoginRequiredMixin,TemplateView):
    template_name = 'authority/auth.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorityGroupView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(AuthorityGroupView, self).get(request, *args, **kwargs)