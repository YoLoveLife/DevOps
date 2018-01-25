# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
import models,forms
from django.urls import reverse_lazy
import os,commands
from xmt.permission import xmt as PermissionXMT
import threading
import query
# Create your views here.
DEPLOY_SCRIPT='/root/xmt/deploy.sh'

def start(CMD,res):
    (status, output) = commands.getstatusoutput(CMD)
    # (status, output) = commands.getstatusoutput('hostname')
    res.result = output
    res.save()
    res.mission.status=1
    res.mission.save()

class XMTCreateView(LoginRequiredMixin,PermissionXMT.XMTAddRequiredMixin,CreateView):
    model = models.XMT
    form_class = forms.XMTForm
    template_name = 'xmt/new_xmt.html'
    success_url = reverse_lazy('xmt:create')

    def get_form(self, form_class=None):
        fm = super(XMTCreateView,self).get_form(form_class=form_class)
        fm.user = self.request.user
        return fm

    def form_valid(self, form):
        result = super(XMTCreateView,self).form_valid(form)
        ENV=form.instance.get_env_display()
        MODULE=form.instance.get_model_display()
        GITLAB=form.instance.gitlab
        CMD = ' %s %s %s'%(ENV,MODULE,GITLAB)
        res = models.XMT_Result(result='未执行完毕')
        res.save()
        form.instance.result = res
        form.instance.save()
        t = threading.Thread(target=start,args=(DEPLOY_SCRIPT + CMD,res))
        t.start()

        return result

    def get_context_data(self, **kwargs):
        context = super(XMTCreateView,self).get_context_data(**kwargs)
        missions = models.XMT.objects.all()[0:10]
        context.update({
            'missions':missions
        })
        return context

    def get_success_url(self):
        return self.success_url

class XMTResultView(LoginRequiredMixin,DetailView):
    model = models.XMT_Result
    template_name = 'xmt/detail_xmt.html'

    def get_context_data(self, **kwargs):
        context=super(XMTResultView,self).get_context_data(**kwargs)
        return context


class XmtStatisticView(LoginRequiredMixin,TemplateView):
    group_id = 2
    template_name = 'xmt/statistics_xmt.html'

    def get_context_data(self, **kwargs):
        context=super(XmtStatisticView,self).get_context_data(**kwargs)

        group = models.Group.objects.filter(id=self.group_id).get()
        users = group.user_set
        deploylist = query.deployQuery(users)

        context.update({
            'deploylist':deploylist,
        })
        return context