# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView,TemplateView


class UtilsManageView(LoginRequiredMixin,TemplateView):
    template_name= 'utils/utils.html'

    def get(self,request,*args, **kwargs):
        return super(UtilsManageView, self).get(request, *args, **kwargs)