# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,UpdateView
from ..models import Group,Permission
from .. import forms
from django.urls import reverse_lazy
# Create your views here.

class AuthorityGroupView(LoginRequiredMixin,TemplateView):
    template_name = 'authority/auth.html'

    def get(self,request,*args, **kwargs):
        return super(AuthorityGroupView, self).get(request, *args, **kwargs)


class AuthorityUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'authority/new_update_auth.html'
    model = Group
    # form_class = forms.HostUpdateForm
    form_class = forms.AuthGroupCreateUpdate
    success_url = reverse_lazy('manager:host')
    def get_context_data(self, **kwargs):
        context = super(AuthorityUpdateView, self).get_context_data(**kwargs)
        permissions = Permission.objects.all()
        permissions_group = [permission.id for permission in self.object.permissions.all()]
        context.update({
            'permissions':permissions,
            'permissions_group':permissions_group,
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(AuthorityUpdateView, self).get(request, *args, **kwargs)