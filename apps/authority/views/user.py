# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse_lazy
from timeline.models import History
from django.contrib.auth.models import Group
from ..permission import user as UserPermission
from .. import models,forms
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView

# Create your views here.
class AuthorityUserView(LoginRequiredMixin,TemplateView):
    template_name = 'authority/user.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorityUserView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(AuthorityUserView, self).get(request, *args, **kwargs)



#AuthorityUserCreateView
class AuthorityUserCreateView(LoginRequiredMixin,UserPermission.UserAddRequiredMixin,CreateView):
    model = models.ExtendUser
    form_class = forms.UserCreateUpdateForm
    template_name = 'authority/new_update_user.html'
    success_url = reverse_lazy('authority:user')

    def form_valid(self, form):
        his=History(user=self.request.user,type=4,info="新增用户",status=0)
        his.save()
        groups=Group.objects.filter(id__in=[2,])
        newuser=form.save()
        newuser.set_password(newuser.password)
        newuser.groups.add(*groups)

        is_active = self.request.POST.get('is_active')
        if is_active == 'actived':
            newuser.is_actuve=1
        else:
            newuser.is_actuve=0

        newuser.save()

        his.status=1
        his.save()
        return super(AuthorityUserCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AuthorityUserCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url



class AuthorityUserUpdateView(LoginRequiredMixin,UserPermission.UserAddRequiredMixin,UpdateView):
    model = models.ExtendUser
    form_class = forms.UserCreateUpdateForm
    template_name = 'authority/new_update_user.html'
    success_url = reverse_lazy('authority:user')

    def form_valid(self, form):
        his=History(user=self.request.user,type=4,info="新增用户",status=0)
        his.save()
        groups=Group.objects.filter(id__in=[2,])
        newuser=form.save()
        newuser.set_password(newuser.password)
        newuser.groups.add(*groups)

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
        is_active = 0
        if self.object.is_active == True:
            is_active = 1
        context.update({
            'is_active':is_active
        })
        return context

    def get_success_url(self):
        return self.success_url

class AuthorityUserDeleteView(LoginRequiredMixin,UserPermission.UserDeleteRequiredMixin,DeleteView):
    model = models.ExtendUser
    success_url = reverse_lazy('authority:user')