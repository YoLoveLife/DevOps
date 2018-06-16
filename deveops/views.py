from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
# from django.shortcuts import redirect,render
#__all__ = ['IndexView','ErrorView','PermissionView']
class IndexView(LoginRequiredMixin,TemplateView):
    template_name = '404.html'
    def get(self,request,*args,**kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

class ErrorView(LoginRequiredMixin,TemplateView):
    template_name = '404.html'
    def get(self,request,*args,**kwargs):
        return super(ErrorView,self).get(request,*args,**kwargs)

class PermissionView(LoginRequiredMixin,TemplateView):
    template_name = 'permission.html'
    def get(self,request,*args,**kwargs):
        return super(PermissionView,self).get(request,*args,**kwargs)