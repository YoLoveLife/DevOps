from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.views.generic import TemplateView
from django.views.generic import View


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    def get(self,request,*args,**kwargs):
        # if not request.user.is_superuser:
        #     return redirect('assets:user-asset-list')
        return super(IndexView, self).get(request, *args, **kwargs)

class ErrorView(LoginRequiredMixin,TemplateView):
    template_name = '404.html'
    def get(self,request,*args,**kwargs):
        return super(ErrorView,self).get(request,*args,**kwargs)

class PermissionView(LoginRequiredMixin,TemplateView):
    template_name = 'permission.html'
    def get(self,request,*args,**kwargs):
        return super(PermissionView,self).get(request,*args,**kwargs)