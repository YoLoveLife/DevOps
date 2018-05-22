# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
import models
PAGE_SIZE=4
# Create your views here.
class TimeLineRecordView(LoginRequiredMixin,TemplateView):
    template_name = 'timeline/record.html'
    #form_class = forms.ScriptForm
    page_size=PAGE_SIZE
    def get_context_data(self, **kwargs):
        context = super(TimeLineRecordView, self).get_context_data(**kwargs)
        hiscount = models.History.objects.all().count()
        pagemax = hiscount/self.page_size
        if pagemax==0:
            pagemax=1
        else:
            pagemax=pagemax+1
        context.update({'hiscount':hiscount,
                        'pagemax':pagemax})
        return context

    def get(self,request,*args, **kwargs):
        return super(TimeLineRecordView, self).get(request, *args, **kwargs)

class TimeLineRecordListView(LoginRequiredMixin,TemplateView):
    template_name = 'timeline/record_list.html'
    page_size = PAGE_SIZE
    def get_context_data(self, **kwargs):
        context = super(TimeLineRecordListView, self).get_context_data(**kwargs)
        page = int(kwargs['pk'])
        historys = models.History.objects.all().order_by('-starttime')[(page-1)*self.page_size:page*self.page_size]
        context.update({'historys':historys})
        return context

    def get(self,request,*args,**kwargs):
        return super(TimeLineRecordListView, self).get(request,*args,**kwargs)

class TimeLineRecordDetailView(LoginRequiredMixin,DetailView):
    template_name = 'timeline/_detail_record.html'
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