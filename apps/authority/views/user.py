# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse_lazy
from timeline.models import History
from ..permission import user as UserPermission
from .. import models,forms
from authority.models import ExtendUser
from django.views.generic.edit import CreateView,UpdateView,DeleteView
#__all__ = ['AuthorityUserCreateView','AuthorityUserUpdateView','AuthorityUserView']
# Create your views here.
from timeline.decorator.manager import decorator_manager
class AuthorityUserView(LoginRequiredMixin,TemplateView):
    template_name = 'authority/user.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorityUserView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(AuthorityUserView, self).get(request, *args, **kwargs)



#AuthorityUserCreateView
class AuthorityUserCreateView(LoginRequiredMixin,UserPermission.UserAddRequiredMixin,CreateView):
    model = ExtendUser
    form_class = forms.UserCreateUpdateForm
    template_name = 'authority/new_update_user.html'
    success_url = reverse_lazy('authority:user')

    @decorator_manager(3,u'新增用户')
    def form_valid(self, form):
        form.before_save(request=self.request,commit=True)
        return self.request.user,super(AuthorityUserCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AuthorityUserCreateView,self).get_context_data(**kwargs)
        auths = Group.objects.all()
        auths_user = []
        context.update({
            'auths':auths,
            'auths_user':auths_user,
        })
        return context

    def get_success_url(self):
        return self.success_url



class AuthorityUserUpdateView(LoginRequiredMixin,UserPermission.UserAddRequiredMixin,UpdateView):
    model = ExtendUser
    form_class = forms.UserCreateUpdateForm
    template_name = 'authority/new_update_user.html'
    success_url = reverse_lazy('authority:user')


    def form_valid(self, form):
        his=History(user=self.request.user,type=3,info="修改用户",status=0)
        his.save()

        newuser=form.save()

        auths_id_list = self.request.POST.getlist('auths',[])
        auths = Group.objects.filter(id__in = auths_id_list)
        newuser.groups.add(*auths)

        is_active = self.request.POST.get('is_active')
        if is_active == 'actived':
            newuser.is_active=1
        else:
            newuser.is_active=0

        newuser.save()

        his.status=1
        his.save()
        return super(AuthorityUserUpdateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AuthorityUserUpdateView,self).get_context_data(**kwargs)
        auths = Group.objects.all()
        auths_user = [group.id for group in self.object.groups.all()]
        context.update({
            'auths':auths,
            'auths_user':auths_user,
        })
        return context

    def get_success_url(self):
        return self.success_url