# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
import forms,models
import permission as UploadPermission
from django.urls import reverse_lazy
from manager.models import Group
from django.views.generic.edit import CreateView
from timeline.decorator.manager import decorator_manager

class UploadGroupFile(LoginRequiredMixin,UploadPermission.UploadAddRequiredMixin,CreateView):
    model = models.GroupUpload
    form_class = forms.GroupUploadFileForm
    template_name = "upload/upload_group.html"
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(UploadGroupFile,self).get_context_data(**kwargs)
        groups = Group.objects.all()
        context.update({
            'groups':groups
        })
        return context

    @decorator_manager(0,u'批量导入主机信息')
    def form_valid(self, form):
        result = self.request.user,super(UploadGroupFile,self).form_valid(form)
        return result

    def get_success_url(self):
        return self.success_url