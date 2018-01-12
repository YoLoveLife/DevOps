# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class DnsListView(TemplateView):
    template_name = 'dns/ddr.html'

    def get(self,request,*args, **kwargs):
        return super(DnsListView, self).get(request, *args, **kwargs)