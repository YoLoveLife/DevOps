# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
import models,forms
from django.urls import reverse_lazy
import os,commands
from xmt.permission import xmt as PermissionXMT
# Create your views here.
DEPLOY_SCRIPT='/root/xmt/deploy.sh'
# DEPLOY_SCRIPT='/tmp/deploy.sh'
import threading
def start(CMD,res):
    (status, output) = commands.getstatusoutput(CMD)
    # (status, output) = commands.getstatusoutput('hostname')
    res.result = output
    res.save()

class XMTCreateView(LoginRequiredMixin,PermissionXMT.XMTAddRequiredMixin,CreateView):
    model = models.XMT
    form_class = forms.XMTForm
    template_name = 'xmt/new_xmt.html'
    success_url = '/xmt/result/'
    result = '0'

    def form_valid(self, form):
        result = super(XMTCreateView,self).form_valid(form)
        ENV=form.instance.get_env_display()
        MODULE=form.instance.get_model_display()
        GITLAB=form.instance.gitlab
        CMD = ' %s %s %s'%(ENV,MODULE,GITLAB)

        t = threading.Thread(target=start,args=(DEPLOY_SCRIPT + CMD,self.res))
        t.start()

        return result

    def get_context_data(self, **kwargs):
        context = super(XMTCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        res = models.XMT_Result(result=u"还没有出现结果")
        res.save()
        self.res = res
        return self.success_url + str(res.id)+'/'

class XMTResultView(LoginRequiredMixin,DetailView):
    model = models.XMT_Result
    template_name = 'xmt/detail_xmt.html'

    def get_context_data(self, **kwargs):
        context=super(XMTResultView,self).get_context_data(**kwargs)
        return context
