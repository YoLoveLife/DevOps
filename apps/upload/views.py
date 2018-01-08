# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
import forms,models
import permission as UploadPermission
from django.urls import reverse_lazy
from manager.models import Group
from django.views.generic.edit import CreateView
from timeline.decorator.manager import decorator_manager
from utils.excel import AnalyzeHostFromExcel,AnalyzeStorageFromExcel

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
        result = super(UploadGroupFile, self).form_valid(form)
        AnalyzeHostFromExcel(form.instance.group.id,form.instance.file)
        return self.request.user,result

    def get_success_url(self):
        return self.success_url


class UploadStorageFile(LoginRequiredMixin,UploadPermission.UploadAddRequiredMixin,CreateView):
    model = models.StorageUpload
    form_class = forms.StorageUploadFileForm
    template_name = "upload/upload_storage.html"
    success_url = reverse_lazy('manager:storage')

    def get_context_data(self, **kwargs):
        context = super(UploadStorageFile,self).get_context_data(**kwargs)
        return context

    @decorator_manager(0,u'批量导入存储信息')
    def form_valid(self, form):
        # form.before_save(request=self.request,commit=True)
        result = super(UploadStorageFile, self).form_valid(form)
        AnalyzeStorageFromExcel(form.instance.file)
        return self.request.user,result

    def get_success_url(self):
        return self.success_url
