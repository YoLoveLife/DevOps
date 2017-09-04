# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
import models
# Create your views here.
class TimeLineRecordView(LoginRequiredMixin,TemplateView):
    template_name = 'timeline/record.html'
    #form_class = forms.ScriptForm

    def get_context_data(self, **kwargs):
        context = super(TimeLineRecordView, self).get_context_data(**kwargs)
        historys = models.History.objects.all().order_by('starttime')
        context.update({'historys':historys})
        return context

    def get(self,request,*args, **kwargs):
        return super(TimeLineRecordView, self).get(request, *args, **kwargs)

class TimeLineRecordDetailView(LoginRequiredMixin,DetailView):
    template_name = 'timeline/detail_record.html'
    model = models.History
    def get_context_data(self, **kwargs):
        context = super(TimeLineRecordDetailView,self).get_context_data(**kwargs)
        history = self.object
        context.update({
            'history':history
        })
        return context

    def get(self,request,*args,**kwargs):
        return super(TimeLineRecordDetailView,self).get(request,*args,**kwargs)

class TimeLinePlanView(LoginRequiredMixin,TemplateView):

    template_name = 'timeline/plan.html'

    def get_context_data(self, **kwargs):
        context = super(TimeLinePlanView,self).get_context_data(**kwargs)
        return context

    def get(self,request,*args,**kwargs):
        return super(TimeLinePlanView,self).get(request,*args,**kwargs)